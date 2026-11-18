import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine

router = APIRouter(tags=["health"])
logger = logging.getLogger(__name__)
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


async def check_postgresql() -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


async def check_redis() -> None:
    await redis_client.ping()


async def _component_status(component: str, check: Callable[[], Awaitable[Any]]) -> dict[str, str]:
    try:
        await check()
    except Exception as exc:
        detail = str(exc) or exc.__class__.__name__
        logger.warning(
            "Readiness check failed",
            extra={"component": component, "detail": detail},
        )
        return {"status": "unavailable", "detail": detail}
    return {"status": "ok"}


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness check; dependency availability is reported separately by /ready."""
    return {"status": "ok"}


@router.get("/ready")
async def readiness() -> JSONResponse:
    """Check PostgreSQL and Redis independently and report component-level status."""
    postgresql, redis = await asyncio.gather(
        _component_status("postgresql", check_postgresql),
        _component_status("redis", check_redis),
    )
    components = {"postgresql": postgresql, "redis": redis}
    ready = all(component["status"] == "ok" for component in components.values())
    return JSONResponse(
        status_code=200 if ready else 503,
        content={"status": "ready" if ready else "not_ready", "components": components},
    )
