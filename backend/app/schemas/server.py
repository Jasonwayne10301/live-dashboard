from pydantic import BaseModel
from typing import Optional


class ServerCreate(BaseModel):
    name: str
    host: str
    port: int = 8000
    protocol: str = "http"
    user: Optional[str] = None
    password: Optional[str] = None
    key: Optional[str] = None
    is_active: bool = True


class ServerOut(ServerCreate):
    id: int

    class Config:
        orm_mode = True
