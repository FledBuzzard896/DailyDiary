from contextlib import asynccontextmanager
from fastapi import FastAPI

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
    license=lifespan
)



# ===== Проверка =====
@app.get("/")
async def root():
    return {"message": "Hello Daily Diary"}
