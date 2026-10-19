import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.utils.logging import LOGGING_CONFIG
from config import settings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("accommodation-service is starting up...")
    yield
    logger.info("accommodation-service is shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/api/accommodations/docs",
        redoc_url="/api/accommodations/redoc",
        openapi_url="/api/accommodations/openapi.json",
    )

    @app.get("/api/accommodations/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
