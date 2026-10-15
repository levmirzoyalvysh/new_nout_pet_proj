from uuid import uuid4


from fastapi import FastAPI , status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_methods=['*'],
                   )


tasks : list[Task]= []
books: list[Book] = []

class Book(BaseModel):

    title: str

class BookCreate(BaseModel):

    title: str

class Task(BaseModel):

    id: str
    title: str
    completed: bool

class CreateTask(BaseModel):

    title: str


@app.get('/')
def read_root():
    return {'massege':'Hello Pidor!'}

@app.get('/tasks',response_model= list[Task])
def read_tasks():
    return tasks

@app.post('/tasks',response_model=Task)
def create_task(payload: CreateTask):
    task = Task(id=str(uuid4()),title=payload.title,completed=False)
    tasks.append(task)
    return task

@app.get('/books', response_model= list[Book])
def get_book():
    return books

@app.post('/books', response_model= Book)
def create_book(payload: BookCreate):
    book = Book(title=payload.title)
    books.append(book)
    return book






