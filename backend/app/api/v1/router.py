from fastapi import APIRouter
from app.api.v1.endpoints import metrics, websocket, auth, server

api_router = APIRouter()
api_router.include_router(metrics.router)
api_router.include_router(websocket.router)
api_router.include_router(auth.router)
api_router.include_router(server.router)
