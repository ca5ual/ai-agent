"""
FastAPI backend для агента "Какой ты котик".

Runner и SessionService создаются один раз при старте приложения и
переиспользуются на все запросы — Runner полностью stateless, изоляция
между пользователями обеспечивается через session_id.
"""

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

from agent.agent import get_agent_for_language

APP_NAME = "cat_personality_app"

app = FastAPI(title="Cat Personality Agent API")

# CORS — на этапе разработки разрешаем всё, на проде сузим до домена фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()

# Кэш runners для каждого языка
runners_cache = {}

def get_runner(language: str = "en"):
    """Получает или создаёт runner для агента выбранного языка."""
    if language not in runners_cache:
        agent = get_agent_for_language(language)
        runners_cache[language] = Runner(
            app_name=APP_NAME,
            agent=agent,
            session_service=session_service,
        )
    return runners_cache[language]


class StartSessionRequest(BaseModel):
    language: str = "ru"


class StartSessionResponse(BaseModel):
    session_id: str
    reply: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    image_url: str | None = None


async def _run_agent_turn(
    session_id: str, user_id: str, message: str, language: str = "ru"
) -> tuple[str, str | None]:
    """Прогоняет одно сообщение пользователя через агента и собирает финальный ответ.

    Важно: результат вызова tool (function_response) обычно приходит в
    отдельном промежуточном событии, а не в финальном текстовом ответе.
    Поэтому image_url ищем по ВСЕМ событиям прохода, а не только там,
    где is_final_response() == True.
    """
    # Сохрани язык в session state, чтобы было видно какой язык используется
    session = await session_service.get_session(session_id)
    if session and not hasattr(session, 'state'):
        session.state = {}
    if session:
        session.state["language"] = language
    
    # Получаем runner для нужного языка
    runner = get_runner(language)
    
    content = types.Content(role="user", parts=[types.Part(text=message)])

    final_text = ""
    image_url = None

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if not event.content or not event.content.parts:
            continue

        for part in event.content.parts:
            if part.function_response:
                response_data = part.function_response.response
                if isinstance(response_data, dict) and response_data.get("image_url"):
                    image_url = response_data["image_url"]

        if event.is_final_response():
            for part in event.content.parts:
                if part.text:
                    final_text += part.text

    return final_text, image_url


@app.post("/api/session/start", response_model=StartSessionResponse)
async def start_session(request: StartSessionRequest):
    """Создаёт новую сессию и получает от агента приветственное сообщение."""
    session_id = str(uuid.uuid4())
    user_id = session_id  # для MVP один пользователь = одна сессия
    language = request.language  # получаем язык из запроса

    try:
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        # "Пинаем" агента пустым приветственным сообщением, чтобы он поздоровался
        # и задал первый вопрос. Передаём язык для использования в ответе.
        reply, _ = await _run_agent_turn(session_id, user_id, "Привет!", language=language)
    except Exception:
        # Полный трейсбек уходит в Cloud Logging (logger.exception сам его
        # приложит), а наружу клиенту — нейтральное сообщение без внутренних
        # деталей (путей, имён сервисов и т.д.)
        logger.exception("Ошибка при старте сессии %s", session_id)
        raise HTTPException(status_code=500, detail="Что-то пошло не так, попробуй ещё раз")

    return StartSessionResponse(session_id=session_id, reply=reply)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Отправляет ответ пользователя агенту и возвращает следующую реплику."""
    user_id = request.session_id  # см. комментарий выше

    try:
        # Получаем язык из session state если он там есть, иначе используем ru
        session = await session_service.get_session(request.session_id)
        language = session.state.get("language", "ru") if session and hasattr(session, 'state') else "ru"
        
        reply, image_url = await _run_agent_turn(
            request.session_id, user_id, request.message, language=language
        )
    except Exception:
        logger.exception("Ошибка при обработке сообщения в сессии %s", request.session_id)
        raise HTTPException(status_code=500, detail="Что-то пошло не так, попробуй ещё раз")

    return ChatResponse(reply=reply, image_url=image_url)