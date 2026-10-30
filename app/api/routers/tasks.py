from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api.dependenses import get_task_service
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskNotFound, TaskService

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


@router.patch("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    service: TaskService = Depends(get_task_service),
) -> TaskSchema:
    try:
        return service.update_task(task_id, payload)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена",
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> None:
    try:
        service.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена",
        )
