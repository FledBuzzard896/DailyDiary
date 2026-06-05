import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORYTHM = os.getenv('ALGORYTHM', "HS256")
ACCESS_TOKEN = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Проверка соответствия введённого пароля хэшу"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Создание хэша пароля"""
    return pwd_context.hash(password)

