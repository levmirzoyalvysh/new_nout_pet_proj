from contextlib import asynccontextmanager
from sqlite3 import dbapi2
from unicodedata import category
from uuid import uuid4
from fastapi import HTTPException, Depends
from fastapi import FastAPI , status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Select, Selectable, select , create_engine
from sqlalchemy.orm import mapped_column, sessionmaker , Session ,DeclarativeBase , Mapped


# подключение к бд докер
DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker[Session](bind=engine)


class Base(DeclarativeBase):

    id : Mapped[str] = mapped_column(primary_key=True,default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = 'tasks'

    title: Mapped[str] 
    completed: Mapped[bool] = mapped_column(default=False)

class CategoryORM(Base):
    __tablename__ = 'categories'

    name: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_methods=['*'],
                   )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    



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


def task_orm_to_model(task_orm: TaskORM)->TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title,completed=task_orm.completed)

def category_orm_to_model(category_orm: CategoryORM)-> CategorySchema:
    return CategorySchema(id= category_orm.id, name= category_orm.name)


@app.get('/tasks',response_model= list[TaskSchema])
def read_tasks(db: Session = Depends(get_db)):
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]

@app.post('/tasks',response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)):
    new_task = TaskORM(title=payload.title,completed=False)
    db.add(new_task)
    db.commit()

    return task_orm_to_model(new_task)

@app.patch('/tasks/{task_id}',response_model=TaskSchema)
def update_task(task_id: str ,payload: TaskUpdateSchema, db: Session = Depends(get_db)):
    task_for_update = db.get(TaskORM, task_id)
    if payload.title is not None:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed

    db.commit()
    return task_for_update

@app.delete('/tasks/{task_id}')
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()

@app.get('/categories', response_model=list[CategorySchema])
def read_categories(db: Session = Depends(get_db)):
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(category_a) for category_a in categories_from_db]

@app.post('/categories',response_model=CategorySchema)
def create_task(payload: CategoryCreateSchema, db: Session = Depends(get_db)):
    new_category = CategoryORM(name=payload.name)
    db.add(new_category)
    db.commit()
    return category_orm_to_model(new_category)


@app.patch('/categories/{category_id}',response_model=CategorySchema)
def update_category(category_id: str , payload: CategoryUpdateSchema, db: Session = Depends(get_db)):
    category_for_update = db.get(CategoryORM, category_id)
    if payload.name is not None:
        category_for_update.name = payload.name
    db.commit()
    return category_for_update

@app.delete('/categories/{category_id}')
def delete_category(category_id : str, db: Session = Depends(get_db)):
    category_for_delete = db.get(CategoryORM,category_id)
    db.delete(category_for_delete)
    db.commit()
    















