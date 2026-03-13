from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.ws_manager import manager
import logging

router = APIRouter(tags=["WebSocket"])
logger = logging.getLogger(__name__)


@router.websocket("/ws/metrics")
async def metrics_ws(websocket: WebSocket):
    """
    WebSocket endpoint for real-time metric snapshots.
    Emits a MetricSnapshot for each server every 2 seconds.

    Connect: ws://localhost:8000/ws/metrics
    """
    await manager.connect(websocket, room="metrics")
    try:
        while True:
            # Keep connection alive; data is pushed by MetricSimulator
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, room="metrics")
        logger.info("Client disconnected from /ws/metrics")


@router.websocket("/ws/alerts")
async def alerts_ws(websocket: WebSocket):
    """
    WebSocket endpoint for real-time alert events.
    Emits AlertEvent when CPU/memory/disk exceeds threshold.

    Connect: ws://localhost:8000/ws/alerts
    """
    await manager.connect(websocket, room="alerts")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, room="alerts")
        logger.info("Client disconnected from /ws/alerts")
