import logging
import random
import threading
import time
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from uuid import uuid4

from google import genai
from google.adk.tools import ToolContext
from google.api_core.exceptions import ResourceExhausted
from google.cloud import storage

from .data import ARCHETYPE_PROMPTS, BLOCK_1, BLOCK_3, QUESTIONS

PROJECT_ID = "ai-agent-cat"
LOCATION = "global"
BUCKET_NAME = "ai-cats-storage-ca5ual"

# Сколько одновременных вызовов к Gemini допускаем
MAX_CONCURRENT_GENERATIONS = 3

# Retry при 429 ошибках
MAX_RETRIES = 5  # ← УВЕЛИЧЕНО с 4
BASE_RETRY_DELAY = 2.0  # ← УВЕЛИЧЕНО с 1.0
MAX_BACKOFF_DELAY = 30.0  # ← ДОБАВЛЕНО: максимальная задержка между retry

GENERATION_TIMEOUT_SECONDS = 120.0  # ← УВЕЛИЧЕНО с 45 (больше времени на всё)

_generation_semaphore = threading.Semaphore(MAX_CONCURRENT_GENERATIONS)
_generation_queue = deque()  # Очередь ожидающих задач
_queue_lock = threading.Lock()
_executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_GENERATIONS + 5)

# Глобальное хранилище статусов генераций
_generation_tasks = {}
_generation_tasks_lock = threading.Lock()

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
        return random.choice(list(ARCHETYPE_PROMPTS.keys()))

    max_score = max(scores.values())
    winners = [archetype for archetype, score in scores.items() if score == max_score]
    return random.choice(winners)


def _generate_archetype_description(client: genai.Client, archetype: str) -> str:
    """Генерирует описание архетипа через LLM."""
    prompt = f"""You are a fun cat personality expert. Write a SHORT, FUNNY description (2-3 sentences max) of what the "{archetype}" cat archetype means.

Focus on personality traits and what it says about this person's cat energy.

Write in VERY plain text, no markdown, no emojis. Don't use difficult words at all. Imagine that you're trying to explain something complex to children. Be playful but concise.

Description:"""
    
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        
        if response.candidates and response.candidates[0].content.parts:
            text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    text += part.text
            return text.strip()
        
        return f"You're a {archetype} cat! That's awesome."
    
    except Exception as exc:
        logger.error(f"Ошибка при генерации описания архетипа {archetype}: {exc}")
        return f"You're a {archetype} cat! That's awesome."


def _generate_image_background(generation_id: str, client: genai.Client, prompt: str, archetype: str):
    """Генерирует картинку в background потоке с полноценным retry.
    
    Этот тред сам отвечает за освобождение семафора через finally,
    даже если клиент уже вернул ответ пользователю.
    """
    enhanced_prompt = f"""{prompt}

CRITICAL REQUIREMENTS FOR THIS IMAGE:
- GENERATE ONLY ONE CAT in the center of the image
- The cat must be the main focus and take up most of the image
- NO OTHER CATS, NO DUPLICATES, NO COMPANIONS
- NO MIRRORS or images of the cat reflected
- Simple white background
- The single cat should be centered and prominent
- Do not include any secondary characters or copies of the cat"""
    
    try:
        last_error = None
        
        for attempt in range(MAX_RETRIES):
            try:
                # Обновляем статус в задаче
                with _generation_tasks_lock:
                    if generation_id in _generation_tasks:
                        _generation_tasks[generation_id]["status"] = "generating"
                        _generation_tasks[generation_id]["attempt"] = attempt + 1
                
                response = client.models.generate_content(
                    model="gemini-3-pro-image",
                    contents=enhanced_prompt,
                )
                
                # Ищем изображение в ответе
                image_bytes = None
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        image_bytes = part.inline_data.data
                        break

                if image_bytes is None:
                    raise ValueError("Модель не вернула изображение")

                # Загружаем в Cloud Storage
                timestamp = int(time.time())
                filename = f"cat_{archetype}_{timestamp}_{generation_id}.png"
                
                storage_client = storage.Client(project=PROJECT_ID)
                bucket = storage_client.bucket(BUCKET_NAME)
                blob = bucket.blob(filename)
                blob.upload_from_string(image_bytes, content_type="image/png")

                image_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

                # Генерируем описание архетипа
                description = _generate_archetype_description(client, archetype)

                # Сохраняем результат ✅
                with _generation_tasks_lock:
                    _generation_tasks[generation_id] = {
                        "status": "success",
                        "archetype": archetype,
                        "image_url": image_url,
                        "description": description,
                    }
                
                logger.info(f"✅ Генерация {generation_id} успешна с попытки {attempt + 1}")
                return

            except ResourceExhausted as exc:
                last_error = exc
                if attempt == MAX_RETRIES - 1:
                    break
                
                # Exponential backoff с джиттером, но не больше MAX_BACKOFF_DELAY
                delay = min(BASE_RETRY_DELAY * (2 ** attempt), MAX_BACKOFF_DELAY)
                delay += random.uniform(0, 1)  # джиттер
                
                logger.warning(
                    f"⚠️ RESOURCE_EXHAUSTED {generation_id}: попытка {attempt + 1}/{MAX_RETRIES}, "
                    f"ждём {delay:.1f}s перед retry..."
                )
                time.sleep(delay)

        # Все попытки исчерпаны ❌
        with _generation_tasks_lock:
            _generation_tasks[generation_id] = {
                "status": "error",
                "message": "Google API quota exhausted. Retried 5 times. Please try again in a few minutes.",
            }
        logger.error(f"❌ Генерация {generation_id} failed после {MAX_RETRIES} попыток")

    except Exception as exc:
        with _generation_tasks_lock:
            _generation_tasks[generation_id] = {
                "status": "error",
                "message": str(exc),
            }
        logger.exception(f"❌ Неожиданная ошибка при генерации {generation_id}")

    finally:
        _generation_semaphore.release()
        logger.info(f"🔓 Семафор освобождён для {generation_id}")


def generate_cat_image(answers: list[str], tool_context: ToolContext) -> dict:
    """Запускает генерацию картинки в background и сразу возвращает generation_id.
    
    Args:
        answers: список из 8 букв (A-H)
        tool_context: контекст сессии ADK
    
    Returns:
        {"status": "generating", "generation_id": "..."}
        или {"status": "error", "message": "..."}
    """
    # Проверяем кэш: может быть, результат уже есть
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

    # Генерируем ID для этой генерации
    generation_id = str(uuid4())

    # Инициализируем статус
    with _generation_tasks_lock:
        _generation_tasks[generation_id] = {
            "status": "generating",
            "started_at": time.time(),
            "attempt": 0,
        }

    # Новые запросы будут ждать, пока не освободится слот
    logger.info(f"⏳ Задача {generation_id} ждёт свободного слота...")
    _generation_semaphore.acquire()  # ← Блокирующее ожидание, БЕЗ timeout
    logger.info(f"🟢 Задача {generation_id} получила слот, запускаем генерацию")

    # Запускаем генерацию в background потоке
    client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION)
    _executor.submit(_generate_image_background, generation_id, client, final_prompt, archetype)

    # Сохраняем generation_id в состояние
    tool_context.state["generation_id"] = generation_id

    return {
        "status": "generating",
        "generation_id": generation_id,
    }


def get_generation_status(generation_id: str) -> dict:
    """Проверяет статус генерации по ID."""
    with _generation_tasks_lock:
        if generation_id not in _generation_tasks:
            return {
                "status": "not_found",
                "message": f"Generation {generation_id} not found",
            }
        return _generation_tasks[generation_id].copy()


def cleanup_old_generations(max_age_seconds: int = 7200):  # ← Увеличено с 3600
    """Очищает старые записи о генерациях."""
    now = time.time()
    with _generation_tasks_lock:
        to_delete = [
            gen_id for gen_id, task in _generation_tasks.items()
            if task.get("started_at") and (now - task["started_at"]) > max_age_seconds
        ]
        for gen_id in to_delete:
            del _generation_tasks[gen_id]
    
    if to_delete:
        logger.info(f"🧹 Очищены {len(to_delete)} старых генераций")