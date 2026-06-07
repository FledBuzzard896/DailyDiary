from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.backend.core.database import get_db
from app.backend.core.security import authenticate_user, ACCESS_TOKEN, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN)
    access_token = create_access_token(
        data={"sub": str(user.id)},
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