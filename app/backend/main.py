from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.backend.routers.tasks import router as task_router
from app.backend.routers.auth import router as auth_router

import asyncpg
import app.backend.core.database as db # Импортируем наш модуль базы данных

@asynccontextmanager
async def lifespan(app: FastAPI):
    # создание пула подключений (при старте приложения)
    db.db_pool = await asyncpg.create_pool(
        dsn=db.DB_URL,
        min_size=1, # минимально 1 соединение
        max_size=10 # максимально 10 одновременных соединений
    )

    yield  # в этой точке приложение работает и принимает запросы

    # код выполняется при остановке приложения
    if db.db_pool:
        await db.db_pool.close()

app = FastAPI(
    title="Daily Diary",
    description="Ежедневник для ваших планов",
    version="1.0",
    lifespan=lifespan
)

app.include_router(task_router)
app.include_router(auth_router)

# ===== Проверка =====
@app.get("/")
async def root():
    return {"message": "Hello Daily Diary"}
