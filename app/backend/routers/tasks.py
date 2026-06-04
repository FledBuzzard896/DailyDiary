from fastapi import FastAPI, APIRouter, HTTPException, Depends

from app.backend.models.tasks import TaskResponse, TaskCreate
from app.backend.core.sql_queries import SELECT_TASK, SELECT_TASKS, CREATE_TASK
from app.backend.core.database import get_db


router = APIRouter(
    tags=["tasks"],
    prefix="/tasks",
    responses={
        404: {"Описание": "Ошибка 404: Я не пойму, что ты  хочешь здесь найти. "},
        200: {"Описание": "Всё выполнено успешно и без происшествий."},
    }
)


@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, db = Depends(get_db)):
    """ Выводит одну задачу по её ID. """
    if 0 < task_id < len(SELECT_TASKS):
        db.execute(SELECT_TASKS, (task_id,))
        return SELECT_TASK[task_id]
    else:
        raise HTTPException(status_code=404, detail="Индекс задачи не найден.")


@router.get("/", response_model=TaskResponse)
async def read_all_tasks():
    """ Выводит все задачи. """
    return SELECT_TASKS


@router.post("/", response_model=TaskCreate)
async def create_task(task: TaskCreate):
    """ Создание задачи. """
    return CREATE_TASK