from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.routes import health
from app.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
        yield test_client


async def test_health_reports_process_liveness(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("failed_component", ["postgresql", "redis"])
async def test_readiness_checks_components_independently_and_returns_503(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch, failed_component: str
) -> None:
    postgresql_check = AsyncMock()
    redis_check = AsyncMock()
    failing_check = postgresql_check if failed_component == "postgresql" else redis_check
    failing_check.side_effect = ConnectionError(f"{failed_component} is offline")
    monkeypatch.setattr(health, "check_postgresql", postgresql_check)
    monkeypatch.setattr(health, "check_redis", redis_check)

    response = await client.get("/ready")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["components"][failed_component] == {
        "status": "unavailable",
        "detail": f"{failed_component} is offline",
    }
    other_component = "redis" if failed_component == "postgresql" else "postgresql"
    assert body["components"][other_component] == {"status": "ok"}
    postgresql_check.assert_awaited_once()
    redis_check.assert_awaited_once()


async def test_readiness_returns_200_when_both_dependencies_are_available(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    postgresql_check = AsyncMock()
    redis_check = AsyncMock()
    monkeypatch.setattr(health, "check_postgresql", postgresql_check)
    monkeypatch.setattr(health, "check_redis", redis_check)

    response = await client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "components": {"postgresql": {"status": "ok"}, "redis": {"status": "ok"}},
    }
    postgresql_check.assert_awaited_once()
    redis_check.assert_awaited_once()
