from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.backend.core.database import get_db
from app.backend.core.security import authenticate_user, ACCESS_TOKEN, create_access_token, get_password_hash
from app.backend.core.sql_queries import SELECT_USER_BY_LOGIN, INSERT_USER
from app.backend.models.users import UserResponse, UserInDB, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)



# ===========================================
#               РЕГИСТРАЦИЯ
# ===========================================
@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db = Depends(get_db)):
    existing = await db.fetchrow(SELECT_USER_BY_LOGIN, user_data.login, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином или email уже существует",
        )

    hashed_password = get_password_hash(user_data.password)

    row = await db.fetchrow(
        INSERT_USER,
        user_data.login,
        hashed_password,
        user_data.name,
        user_data.surname,
        user_data.email
    )

    if not row:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать пользователя",
        )

    return UserResponse(**dict(row))



# ===========================================
#               АВТОРИЗАЦИЯ
# ===========================================
@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN)
    access_token = create_access_token(
        data={"sub": str(user["id"])},
        expires_delta=access_token_expires
    )
    return {"token": access_token, "token_type": "bearer"}

"""
from_data - Объект, содержащий поля username, password (и опционально scope, client_id и т.д.), переданные в теле запроса в формате x-www-form-urlencoded.
            Depends(OAuth2PasswordRequestForm) — FastAPI автоматически парсит входящий запрос и предоставляет эти данные.
timedelta(minutes=ACCESS_TOKEN) - интервал времени, через который токен истечёт.
create_access_token — функция, которая:
 - Копирует переданные data (здесь {"sub": str(user.id)}).
 - Добавляет поле exp (время истечения) — текущее UTC-время + expires_delta.
 - Подписывает токен с помощью SECRET_KEY и алгоритма (например, HS256).
 - Возвращает строку токена (например, eyJhbGciOiJIUzI1NiIs...).
"""