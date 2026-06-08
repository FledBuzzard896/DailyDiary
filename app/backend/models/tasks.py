from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, computed_field


# Модели для task_status
class StatusBase(BaseModel):
    title: str = Field(..., max_length=50, description="Название статуса")

class StatusCreate(StatusBase):
    pass

class StatusUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=50)

class StatusResponse(StatusBase):
    id: int

    class Config:
        from_attributes = True


# Модели для tasks
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    deadline: Optional[datetime] = Field(None, description="Дедлайн (с учётом часового пояса)")

class TaskCreate(TaskBase):
    # user_id и status_id обычно назначаются сервером (status_id по умолчанию = 2)
    status_id: int = Field(2, description="ID статуса (по умолчанию 'В процессе')")
    user_id: Optional[int] = None  # может быть установлен из контекста

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    # Виртуальное поле для удобства клиента (будет преобразовано в status_id + completed_at)
    is_completed: Optional[bool] = Field(None, description="Отметить задачу выполненной")

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    user_id: int
    status_id: int
    is_deleted: bool = False

    @computed_field
    @property
    def is_completed(self) -> bool:
        """Вычисляемое поле: задача считается выполненной, если статус = 1 (Выполнено)"""
        return self.status_id == 1

    class Config:
        from_attributes = True
