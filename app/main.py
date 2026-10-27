from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.tasks import router as tasks_router
from app.api.routers.categories import router as category_router



app = FastAPI()
app.include_router(router=tasks_router)
app.include_router(router=category_router)

app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_methods=['*'],
                   )

    















