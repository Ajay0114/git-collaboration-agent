from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings.log_level)
    yield
    await health.redis_client.aclose()
    await engine.dispose()


app = FastAPI(
    title="Git Collaboration Intelligence Agent",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(health.router)
