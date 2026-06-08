from fastapi import APIRouter, HTTPException, Depends

from app.backend.core.security import get_current_user
from app.backend.models.tasks import TaskResponse, TaskCreate
from app.backend.core.sql_queries import SELECT_TASK, SELECT_TASKS, CREATE_TASK
from app.backend.core.database import get_db


router = APIRouter(
    tags=["tasks"],
    prefix="/tasks",
    responses={
        200: {"Описание": "Всё выполнено успешно и без происшествий."},
        400: {"Описание": "Неверный запрос."},
        404: {"Описание": "Ошибка 404: Я не пойму, что ты  хочешь здесь найти. "},
        500: {"Описание": "Внутренняя ошибка сервера."},
    }
)


@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, db = Depends(get_db)):
    """ Выводит одну задачу по её ID. """
    row = await db.fetchrow(SELECT_TASK, task_id)

    if not row:
        raise HTTPException(status_code=404, detail="Индекс задачи не найден.")
    return dict(row)


@router.get("/", response_model=list[TaskResponse])
async def read_all_tasks(db = Depends(get_db)):
    """ Выводит все задачи. """
    rows = await db.fetch(SELECT_TASKS)

    if not rows:
        raise HTTPException(status_code=404, detail="Задачи не найдены. ")
    return [dict(row) for row in rows] # конвертация строки Record в словарь


@router.post("/", response_model=TaskCreate)
async def create_task(task: TaskCreate,
                      db = Depends(get_db),
                      current_user = Depends(get_current_user)):
    """ Создание задачи. """
    if task.status_id is not None:
        status_id = task.status_id
    row = await db.fetchrow(CREATE_TASK,
                            task.title, task.description, task.deadline,
                            current_user.id, status_id)
    if not row:
        raise HTTPException(500, "Не удалось создать задачу")
    return TaskResponse(**dict(row))
