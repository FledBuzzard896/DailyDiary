from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


# Модели для users
class UserBase(BaseModel):
    login: str = Field(..., min_length=1, max_length=50, description="Уникальный логин")
    name: str = Field(..., min_length=1, max_length=50, description="Имя")
    surname: Optional[str] = Field(None, max_length=50, description="Фамилия")
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Пароль")

class UserUpdate(BaseModel):
    login: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    surname: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    # Пароль не возвращаем

    class Config:
        from_attributes = True   # for ORM (SQLAlchemy) or from_dict

class UserInDB(UserBase):
    """Модель пользователя, который хранится в базе данных."""
    id: int
    hashed_password: str

class Token(BaseModel):
    """Модель для ответа с токеном."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Модель для данных, хранящихся внутри токена."""
    user_id: Optional[int] = None