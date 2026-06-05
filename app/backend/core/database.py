import os
import asyncpg
from dotenv import load_dotenv

load_dotenv() # берёт переменные из .env

DB_URL = os.getenv("DATABASE_CONFIG")

db_pool : asyncpg.Pool | None = None
async def get_db():
    """
    Функция-зависимость для FastAPI.
    Выдает живое подключение из пула и автоматически закрывает его после работы ручки.
    """
    if db_pool is None:
        raise RuntimeError("Пул подключений к базе данных не инициализирован.")

    async with db_pool.acquire() as connection:
        # Открываем транзакцию. Если внутри ручки случится ошибка,
        # asyncpg автоматически сделает ROLLBACK. Если всё ок — COMMIT.
        async with connection.transaction():
            yield connection