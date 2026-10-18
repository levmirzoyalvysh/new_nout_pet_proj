from uuid import uuid4


from fastapi import FastAPI , status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_methods=['*'],
                   )


tasks : list[TaskSchema] = []


class Category(BaseModel):

    id: str
    title: str
    completed: bool


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

@app.delete('/tasks/{task_id}')
def delete_task(task_id: str):
    for task in tasks:
        if task_id == task.id:
            tasks.remove(task)
            return










