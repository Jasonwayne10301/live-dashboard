import pytest
import os
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# Set test database URL BEFORE any imports
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment before all tests."""
    yield


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def mock_simulator(monkeypatch):
    """Mock the metric simulator."""
    mock_sim = MagicMock()
    mock_sim.start = AsyncMock(return_value=None)
    mock_sim.stop = AsyncMock(return_value=None)
    mock_sim.client_count = MagicMock(return_value=0)
    
    monkeypatch.setattr("app.core.simulator.simulator", mock_sim)
    yield mock_sim


@pytest.fixture
async def client(mock_simulator, monkeypatch):
    """Create a test client with seeded test data."""
    # Import app modules AFTER environment is set
    from app.core.database import AsyncSessionLocal, Base, engine
    from app.models.server import ServerConfig
    from app.main import app
    from sqlalchemy import select
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed test data
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ServerConfig))
        existing = result.scalars().all()
        
        if not existing:
            servers_data = [
                {"name": "server-01", "host": "192.168.1.10", "port": 8000, "is_active": True},
                {"name": "server-02", "host": "192.168.1.11", "port": 8000, "is_active": True},
                {"name": "server-03", "host": "192.168.1.12", "port": 8000, "is_active": True},
            ]
            for server_data in servers_data:
                server = ServerConfig(**server_data)
                session.add(server)
            await session.commit()
    
    # Create test client
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()



