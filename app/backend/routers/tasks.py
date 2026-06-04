from fastapi import APIRouter, HTTPException, Depends

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
    db.execute(SELECT_TASKS, (task_id,))
    task = db.fetchone()

    if not task:
        raise HTTPException(status_code=404, detail="Индекс задачи не найден.")
    return task


@router.get("/", response_model=list[TaskResponse])
async def read_all_tasks(db = Depends(get_db)):
    """ Выводит все задачи. """
    db.execute(SELECT_TASKS)
    tasks = db.fetchall()

    if not tasks:
        raise HTTPException(status_code=404, detail="Задачи не найдены. ")
    return tasks


@router.post("/", response_model=TaskCreate)
async def create_task(task: TaskCreate,
                      db = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """ Создание задачи. """
    if task.status_id is not None:
        status_id = task.status_id
    values = (
        task.title,
        task.description,
        task.deadline,
        current_user.id,
        status_id,
    )

    try:
        row = await db.execute(CREATE_TASK, *values)
        if not row:
            raise HTTPException(status_code=500, detail="Сервер: Создание задачи завершилось ошибкой.")
        return TaskResponse(**dict(row))
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Ошибка в запросе: {str(error)}")
