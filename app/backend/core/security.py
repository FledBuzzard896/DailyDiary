import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext # класс со схемами хеширования

from app.backend.core.database import get_db
from app.backend.core.sql_queries import SELECT_USER_BY_LOGIN, SELECT_USER_BY_ID

load_dotenv()

# Точка входа для получения токена из заголовка Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")  # URL вашего эндпоинта логина

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORYTHM = os.getenv('ALGORYTHM', "HS256")
ACCESS_TOKEN = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
schemes=["bcrypt"] - Список алгоритмов хеширования, которые будет использовать контекст.
    Здесь указан только bcrypt – современный, устойчивый к перебору алгоритм (он автоматически добавляет "соль" и делает хеш медленным).
deprecated="auto"  - Указывает, как обрабатывать хеши, сделанные устаревшими алгоритмами.
    "auto" означает, что контекст сам определит, какой из перечисленных алгоритмов считается устаревшим (если в schemes несколько).
    Так вы можете постепенно переводить пользователей на более новый алгоритм.
"""

def verify_password(plain_password, hashed_password):
    """Проверка соответствия введённого пароля хэшу"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Создание хэша пароля"""
    return pwd_context.hash(password)

async def authenticate_user(db, login: str, password: str):
    """Находит пользователя в БД по логину и проверяет пароль."""
    user = await db.fetchrow(SELECT_USER_BY_LOGIN, login)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Создает новый JWT-токен."""
    to_encode = data.copy()                                                     # копируем полезные данные (обычно словарь)
    if expires_delta:                                                           # установка время жизни токена
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN)
    to_encode.update({"exp": expire})                                           # добавляем поле "exp" (время истечения)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)        # кодировка токена
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Декодируем токен и извлекаем user_id
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 2. Ищем пользователя в БД по id
    user = await db.fetchrow(SELECT_USER_BY_ID, user_id)
    if user is None:
        raise credentials_exception
    return user