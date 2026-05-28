from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# база задачи
class TaskBase(BaseModel):
    description: Optional[str] = Field(None, max_length=200, description="Описание, дополнительные сведения задачи")

# создание задачи
class TaskCreate(TaskBase):
    title: str = Field(..., min_length=1, max_length=100, description="Название задачи")

# обновление задачи
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Новое название")
    description: Optional[str] = Field(None, max_length=200, description="Новое описание")
    is_completed: Optional[bool] = Field(None, description="Статус выполнения")

# ответ пользователю
class TaskResponse(TaskBase):
    task_id: int
    title: str
    user_id: int
    is_completed: bool = False
    created_at: datetime
