import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from internal_middleware import (
    build_request_id_middleware,
    build_user_context_middleware,
)

from app.client.gateway_client import GatewayClient
from app.routes.accommodation_routes import router as accommodation_router
from app.routes.admin_routes import router as admin_router
from app.routes.references_routes import router as references_router
from app.utils.logging import LOGGING_CONFIG
from config import settings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("accommodation-service is starting up...")
    app.state.gateway_client = GatewayClient()
    try:
        yield
    finally:
        await app.state.gateway_client.close()
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

    app.middleware("http")(build_request_id_middleware(logger=logger))
    app.middleware("http")(build_user_context_middleware(logger=logger))

    @app.get("/api/accommodations/health")
    async def health_check():
        return {"status": "ok"}

    app.include_router(accommodation_router)
    app.include_router(references_router)
    app.include_router(admin_router)

    return app


app = create_app()
