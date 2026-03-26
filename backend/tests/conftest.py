import pytest
import os
import sys
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# Set test database URL to use a file-based SQLite database for test isolation
# This works better than in-memory for multi-connection scenarios
test_db_path = os.path.join(
    os.path.dirname(__file__), "..", ".test_db.sqlite"
)
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{test_db_path}"

# Remove any cached app modules to force re-import with new DATABASE_URL
for key in list(sys.modules.keys()):
    if key.startswith("app"):
        del sys.modules[key]


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment before all tests."""
    # Clean up test database if it exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    yield
    # Clean up after all tests
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


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
    # Import app modules AFTER environment is set and cached modules cleared
    from app.core.database import AsyncSessionLocal, Base, engine
    from app.models.server import ServerConfig
    from app.main import app
    from sqlalchemy import select
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed test data
    async with AsyncSessionLocal() as session:
        # Check if servers already exist
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




