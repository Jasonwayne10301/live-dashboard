import pytest
import os
from unittest.mock import AsyncMock, patch
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session", autouse=True)
def configure_test_env():
    """Configure environment for testing before any imports."""
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    yield
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def mock_simulator(monkeypatch):
    """Mock the metric simulator to prevent continuous background tasks."""
    from app.core import simulator as sim_module
    
    # Mock the simulator instance
    mock_sim = AsyncMock()
    mock_sim.start = AsyncMock(return_value=None)
    mock_sim.stop = AsyncMock(return_value=None)
    mock_sim.client_count = AsyncMock(return_value=0)
    mock_sim.SERVERS = {
        "server-01": AsyncMock(),
        "server-02": AsyncMock(),
        "server-03": AsyncMock(),
    }
    
    monkeypatch.setattr(sim_module, "simulator", mock_sim)
    yield mock_sim


@pytest.fixture
async def test_app():
    """Create test FastAPI app instance."""
    from app.main import app
    from app.core.database import AsyncSessionLocal, engine, Base
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield app
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

