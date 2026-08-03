"""
Tool-функция, которую ADK-агент вызывает после сбора всех 8 ответов.
Вся логика подсчёта архетипа и вызова модели генерации изображений
находится здесь — она полностью детерминирована и не проходит через LLM.
"""

import logging
import random
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

from google import genai
from google.adk.tools import ToolContext
from google.api_core.exceptions import ResourceExhausted
from google.cloud import storage

from .data import ARCHETYPE_PROMPTS, BLOCK_1, BLOCK_3, QUESTIONS

PROJECT_ID = "ai-agent-cat"
LOCATION = "global"
BUCKET_NAME = "ai-cats-storage-ca5ual"

# Сколько одновременных вызовов к Gemini допускаем с одного инстанса
# Cloud Run. Если сюда прилетит concurrency=80, все 80 запросов не
# должны одновременно долбить Vertex AI — иначе гарантированный 429.
MAX_CONCURRENT_GENERATIONS = 3
GENERATION_TIMEOUT_SECONDS = 20.0
MAX_RETRIES = 4
BASE_RETRY_DELAY = 1.0

_generation_semaphore = threading.Semaphore(MAX_CONCURRENT_GENERATIONS)
_executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_GENERATIONS + 2)

logger = logging.getLogger(__name__)


def _calculate_archetype(answers: list[str]) -> str:
    """Считает баллы по архетипам на основе 8 ответов (список букв A-H)."""
    scores = defaultdict(int)
    for question, letter in zip(QUESTIONS, answers):
        letter = letter.strip().upper()
        option = question["options"].get(letter)
        if option is None:
            continue
        scores[option["archetype"]] += 1

    if not scores:
        # На случай, если что-то пошло не так со сбором ответов
        return random.choice(list(ARCHETYPE_PROMPTS.keys()))

    max_score = max(scores.values())
    winners = [archetype for archetype, score in scores.items() if score == max_score]
    return random.choice(winners)


def _call_gemini_with_retry(client: genai.Client, prompt: str):
    """Вызывает generate_content с exponential backoff на 429 ошибках.

    Квота на Vertex AI считается по окну в минуту, поэтому короткая
    пауза перед повтором обычно решает проблему без вмешательства юзера.
    """
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            return client.models.generate_content(
                model="gemini-3-pro-image",
                contents=prompt,
            )
        except ResourceExhausted as exc:
            last_error = exc
            if attempt == MAX_RETRIES - 1:
                break
            delay = BASE_RETRY_DELAY * (2 ** attempt) + random.uniform(0, 0.5)
            logger.warning(
                "RESOURCE_EXHAUSTED от Vertex AI, попытка %d/%d, retry через %.1fs",
                attempt + 1, MAX_RETRIES, delay,
            )
            time.sleep(delay)

    raise last_error


def generate_cat_image(answers: list[str], tool_context: ToolContext) -> dict:
    """Генерирует изображение кота-архетипа на основе ответов пользователя.

    Args:
        answers: список из 8 букв (A-H), по одной на каждый вопрос,
            в том порядке, в котором были заданы вопросы 1-8.
        tool_context: передаётся ADK автоматически, даёт доступ к состоянию
            текущей сессии — используется, чтобы не генерировать картинку
            повторно, если тест для этой сессии уже пройден.

    Returns:
        Словарь с путём к сохранённому файлу изображения, названием
        архетипа на русском, и статусом выполнения.
    """
    # Защита от повторной генерации: если для этой сессии уже есть готовый
    # результат — отдаём его снова, не тратя ещё один платный вызов модели
    cached = tool_context.state.get("cat_result")
    if cached is not None:
        return cached

    if len(answers) != 8:
        return {
            "status": "error",
            "message": f"Ожидалось 8 ответов, получено {len(answers)}",
        }

    archetype = _calculate_archetype(answers)
    final_prompt = f"{BLOCK_1}\n\n{ARCHETYPE_PROMPTS[archetype]}\n\n{BLOCK_3}"

    client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION)

    # Ограничиваем, сколько запросов одновременно уходит к Vertex AI с
    # этого инстанса. Если лимит занят — ждём слот, а не бомбим API.
    acquired = _generation_semaphore.acquire(timeout=GENERATION_TIMEOUT_SECONDS)
    if not acquired:
        logger.error("Не дождались свободного слота генерации, все заняты")
        return {
            "status": "error",
            "message": "Сервис сейчас перегружен, попробуйте через минуту",
        }

    try:
        future = _executor.submit(_call_gemini_with_retry, client, final_prompt)
        try:
            response = future.result(timeout=GENERATION_TIMEOUT_SECONDS)
        except FutureTimeoutError:
            logger.error("Таймаут генерации изображения (%.0fs)", GENERATION_TIMEOUT_SECONDS)
            return {
                "status": "error",
                "message": "Генерация заняла слишком много времени, попробуйте ещё раз",
            }
        except ResourceExhausted:
            logger.error("Квота Vertex AI исчерпана после всех попыток retry")
            return {
                "status": "error",
                "message": "Сервис генерации временно недоступен, попробуйте через пару минут",
            }
    finally:
        _generation_semaphore.release()

    image_bytes = None
    filename = None

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            timestamp = int(time.time())
            filename = f"cat_{archetype}_{timestamp}.png"
            image_bytes = part.inline_data.data
            break

    if image_bytes is None:
        return {
            "status": "error",
            "message": "Модель не вернула изображение",
        }

    # Загружаем картинку сразу в Cloud Storage — без промежуточного
    # сохранения на диск контейнера (в Cloud Run диск не персистентный)
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type="image/png")

    image_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    result = {
        "status": "success",
        "archetype": archetype,
        "image_url": image_url,
    }

    # Сохраняем результат в состояние сессии, чтобы повторные вызовы
    # (например, если агент случайно попытается вызвать tool снова)
    # не генерировали новую картинку, а отдавали уже готовую
    tool_context.state["cat_result"] = result

    return result