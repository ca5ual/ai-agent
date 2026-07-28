"""
Tool-функция, которую ADK-агент вызывает после сбора всех 8 ответов.
Вся логика подсчёта архетипа и вызова модели генерации изображений
находится здесь — она полностью детерминирована и не проходит через LLM.
"""

import random
import time
from collections import defaultdict

from google import genai
from google.adk.tools import ToolContext
from google.cloud import storage

from .data import ARCHETYPE_NAMES_RU, ARCHETYPE_PROMPTS, BLOCK_1, BLOCK_3, QUESTIONS

PROJECT_ID = "ai-cats-502309"
LOCATION = "global"
BUCKET_NAME = "ai-cats-storage"


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
    archetype_name_ru = ARCHETYPE_NAMES_RU[archetype]

    final_prompt = f"{BLOCK_1}\n\n{ARCHETYPE_PROMPTS[archetype]}\n\n{BLOCK_3}"

    client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION)

    response = client.models.generate_content(
        model="gemini-3-pro-image",
        contents=final_prompt,
    )

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
        "archetype_name_ru": archetype_name_ru,
        "image_url": image_url,
    }

    # Сохраняем результат в состояние сессии, чтобы повторные вызовы
    # (например, если агент случайно попытается вызвать tool снова)
    # не генерировали новую картинку, а отдавали уже готовую
    tool_context.state["cat_result"] = result

    return result