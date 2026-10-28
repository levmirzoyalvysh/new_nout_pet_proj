from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.categories import router as category_router
from app.api.routers.tasks import router as tasks_router
from app.core.config import get_settings
from app.core.logging import configure_logging, logging

configure_logging()

_total = 0

settings = get_settings()
app = FastAPI()
logger = logging.getLogger("app.middleware")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def num_requests(request: Request, call_next) -> Response:
    global _total
    _total += 1
    logger.info(
        "Request: %s %s",
        request.method,
        request.url.path,
    )
    response: Response = await call_next(request)
    response.headers["x-request-number"] = str(_total)
    return response


@app.middleware(
    "http"
)  # log_requests выполнится до и после обработки каждого HTTP-запроса
async def sad_requests(request: Request, call_next) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)  # Работа самого эндпоинта
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f милисекунд)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


app.include_router(router=tasks_router)
app.include_router(router=category_router)
