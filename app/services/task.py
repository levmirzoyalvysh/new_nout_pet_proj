from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema


class TaskNotFound(Exception):
    pass


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    def update_task(self, task_id, task_update: TaskUpdateSchema):
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        return TaskSchema.model_validate(task_for_update)

    def create_task(self, task_create) -> TaskCreateSchema:
        task_orm_cr = self.task_repository.create_task(title=task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm_cr)

    def delete_task(self, task_id):
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        self.task_repository.delete_task(task_for_delete)
        self.db.commit()
