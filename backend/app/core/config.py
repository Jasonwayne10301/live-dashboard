from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Live Dashboard API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Real-time system metrics dashboard powered by FastAPI WebSocket"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    USE_REAL_METRICS: bool = False
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "live_dashboard"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Simulator
    METRIC_EMIT_INTERVAL: float = 2.0   # seconds between metric pushes
    ALERT_THRESHOLD_CPU: float = 85.0
    ALERT_THRESHOLD_MEMORY: float = 80.0
    ALERT_THRESHOLD_DISK: float = 90.0
    USE_REAL_METRICS: bool = True  # Set True to use real system metrics instead of simulated
    REMOTE_SERVERS: dict = {  # Example: {'server-01': {'host': '192.168.1.10', 'user': 'user', 'key': '/path/to/key'}}
        'server-01': {'host': 'localhost', 'user': '', 'password': ''},  # Local for demo
        'server-02': {'host': '172.22.234.101', 'port': 8001, 'protocol': 'http'},  # WSL HTTP
        'server-03': {'host': 'localhost', 'user': '', 'password': ''},
    }

    class Config:
        env_file = ".env"


settings = Settings()
