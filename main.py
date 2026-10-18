from uuid import uuid4
from fastapi import HTTPException


from fastapi import FastAPI , status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_methods=['*'],
                   )


tasks : list[TaskSchema] = []
categories: list[CategorySchema] = []


class CategorySchema(BaseModel):

    id: str
    name: str

class CategoryCreateSchema(BaseModel):

    name: str

class CategoryUpdateSchema(BaseModel):

    name: str | None = None


class TaskSchema(BaseModel):

    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):

    title: str

class TaskUpdateSchema(BaseModel):

    title: str | None = None
    completed: bool | None = None




@app.get('/')
def read_root():
    return {'massege':'Hello Pidor!'}

@app.get('/tasks',response_model= list[TaskSchema])
def read_tasks():
    return tasks

@app.post('/tasks',response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema):
    task = TaskSchema(id=str(uuid4()),title=payload.title,completed=False)
    tasks.append(task)
    return task

@app.patch('/tasks/{task_id}',response_model=TaskSchema)
def update_task(task_id: str ,payload: TaskUpdateSchema):
    for task in tasks:
        if task_id == task.id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed

            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

@app.delete('/tasks/{task_id}')
def delete_task(task_id: str):
    for task in tasks:
        if task_id == task.id:
            tasks.remove(task)
            return


@app.get('/categories', response_model=list[CategorySchema])
def read_categories():
    return categories

@app.post('/categories',response_model=CategorySchema)
def create_task(payload: CategoryCreateSchema):
    new_category = CategorySchema(id=str(uuid4()),name=payload.name)
    categories.append(new_category)
    return new_category

@app.patch('/categories/{category_id}',response_model=CategorySchema)
def update_category(category_id: str , payload: CategoryUpdateSchema):
    for category in categories:
        if category_id == category.id:
            if payload.name is not None:
                category.name = payload.name
            return category


@app.delete('/categories/{category_id}')
def delete_category(category_id : str):
    for category in categories:
        if category_id == category.id:
            categories.remove(category)
        return 















