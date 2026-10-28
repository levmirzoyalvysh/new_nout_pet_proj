from fastapi import APIRouter, Depends, status

from app.api.dependenses import get_task_service
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskService

router = APIRouter()


@router.get("/tasks")
def read_tasks(
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskSchema]:
    return task_service.list_tasks()


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateSchema, task_service: TaskService = Depends(get_task_service)
):
    return task_service.create_task(task_create=payload)


@router.patch("/tasks/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.update_task(task_id=task_id, task_update=payload)


@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)):
    return task_service.delete_task(task_id=task_id)
