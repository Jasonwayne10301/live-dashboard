from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class ServerConfig(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False, default=8000)
    protocol = Column(String(10), nullable=False, default="http")
    user = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    key = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
