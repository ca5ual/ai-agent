"""
FastAPI backend с поддержкой асинхронной генерации.
"""

import asyncio
import logging
import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cat_agent_api")

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), "agent", ".env"),
    override=True,
)

from agent.agent import root_agent
from agent.tools import get_generation_status, cleanup_old_generations

APP_NAME = "cat_personality_app"

app = FastAPI(title="Cat Personality Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()
runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service,
)


class StartSessionResponse(BaseModel):
    session_id: str
    reply: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    generation_id: str | None = None  # ID для отслеживания генерации


class GenerationStatusResponse(BaseModel):
    status: str  # "generating", "success", "error", "not_found"
    archetype: str | None = None
    image_url: str | None = None
    message: str | None = None


async def _run_agent_turn(session_id: str, user_id: str, message: str) -> tuple[str, str | None]:
    """Прогоняет сообщение пользователя через агента.
    
    Теперь возвращает generation_id вместо image_url, так как картинка
    будет готова позже.
    """
    content = types.Content(role="user", parts=[types.Part(text=message)])

    final_text = ""
    generation_id = None

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if not event.content or not event.content.parts:
            continue

        for part in event.content.parts:
            if part.function_response:
                response_data = part.function_response.response
                if isinstance(response_data, dict):
                    if response_data.get("status") == "generating":
                        generation_id = response_data.get("generation_id")
                    elif response_data.get("status") == "error":
                        # Ошибка при вызове тула
                        final_text += f"\n\n⚠️ {response_data.get('message', 'Ошибка')}"

        if event.is_final_response():
            for part in event.content.parts:
                if part.text:
                    final_text += part.text

    return final_text, generation_id


@app.post("/api/session/start", response_model=StartSessionResponse)
async def start_session():
    """Создаёт новую сессию и получает приветствие от агента."""
    session_id = str(uuid.uuid4())
    user_id = session_id

    try:
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        reply, _ = await _run_agent_turn(session_id, user_id, "Привет!")
    except Exception:
        logger.exception("Ошибка при старте сессии %s", session_id)
        raise HTTPException(status_code=500, detail="Что-то пошло не так, попробуй ещё раз")

    return StartSessionResponse(session_id=session_id, reply=reply)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Отправляет ответ пользователя агенту.
    
    Если агент вызвал generate_cat_image, вернёт generation_id.
    Клиент потом может проверять статус через /api/generation/{generation_id}
    """
    user_id = request.session_id

    try:
        reply, generation_id = await _run_agent_turn(
            request.session_id, user_id, request.message
        )
    except Exception:
        logger.exception("Ошибка при обработке сообщения в сессии %s", request.session_id)
        raise HTTPException(status_code=500, detail="Что-то пошло не так, попробуй ещё раз")

    return ChatResponse(reply=reply, generation_id=generation_id)


@app.get("/api/generation/{generation_id}", response_model=GenerationStatusResponse)
async def check_generation_status(generation_id: str):
    """Проверяет статус генерации изображения.
    
    Клиент может вызывать этот endpoint периодически (например, каждые 500ms),
    пока статус не станет "success" или "error".
    
    Returns:
        {
            "status": "generating" | "success" | "error" | "not_found",
            "image_url": "https://..." (если успешно),
            "message": "Описание ошибки" (если ошибка),
            "archetype": "NameOfArchetype" (если успешно)
        }
    """
    try:
        status_data = get_generation_status(generation_id)
        return GenerationStatusResponse(**status_data)
    except Exception:
        logger.exception("Ошибка при проверке статуса %s", generation_id)
        raise HTTPException(status_code=500, detail="Ошибка при проверке статуса")


@app.get("/api/health")
async def health_check():
    """Проверка здоровья сервиса."""
    return {"status": "ok"}


# Периодическая очистка старых генераций
@app.on_event("startup")
async def startup_cleanup():
    """Запускает фоновую задачу очистки."""
    async def cleanup_loop():
        while True:
            await asyncio.sleep(600)  # каждые 10 минут
            cleanup_old_generations(max_age_seconds=3600)  # удаляем старше часа
    
    asyncio.create_task(cleanup_loop())