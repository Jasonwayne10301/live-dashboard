import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


async def test_list_servers(client: AsyncClient):
    response = await client.get("/api/v1/metrics/servers")
    assert response.status_code == 200
    data = response.json()
    assert "servers" in data
    assert len(data["servers"]) == 3
    assert "server-01" in data["servers"]


async def test_get_history_unknown_server(client: AsyncClient):
    response = await client.get("/api/v1/metrics/history/unknown-server")
    assert response.status_code == 200
    assert "error" in response.json()


async def test_summary_returns_list(client: AsyncClient):
    response = await client.get("/api/v1/metrics/summary")
    assert response.status_code == 200
    assert "servers" in response.json()


async def test_connection_stats(client: AsyncClient):
    response = await client.get("/api/v1/metrics/stats/connections")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "metrics_room" in data
