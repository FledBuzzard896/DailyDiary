import os
import psycopg2
from psycopg2.extras import RealDictCursor # Получение результатов из БД
from dotenv import load_dotenv

load_dotenv() # берёт переменные из .env

DB_CONFIG = os.getenv("DATABASE_CONFIG")

def get_db():
    connection = None
    try:
        connection = psycopg2.connect(DB_CONFIG)
        # RealDictCursor нужен, чтобы строки из БД возвращались как {'id': 1, 'title': 'Запись'}
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        # Передаем управление в ручку FastAPI
        yield cursor
        # Если всё прошло успешно, сохраняем изменения
        connection.commit()
    except Exception as error:
        if connection:
            connection.rollback() # откат изменений при ошибке
        print(f"Ошибка базы данных: {error}")
        raise error
    finally:
        # В любом случае закрываем соединение после выполнения ручки
        if connection:
            cursor.close()
            connection.close()