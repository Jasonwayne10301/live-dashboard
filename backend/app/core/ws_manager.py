from fastapi import WebSocket
from typing import Dict, Set
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages all active WebSocket connections.
    Supports broadcasting to all clients or targeting specific rooms.
    """

    def __init__(self):
        # room_id -> set of websockets
        self._rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str = "global") -> None:
        await websocket.accept()
        self._rooms.setdefault(room, set()).add(websocket)
        logger.info(f"Client connected to room '{room}'. Total in room: {len(self._rooms[room])}")

    def disconnect(self, websocket: WebSocket, room: str = "global") -> None:
        if room in self._rooms:
            self._rooms[room].discard(websocket)
            if not self._rooms[room]:
                del self._rooms[room]
        logger.info(f"Client disconnected from room '{room}'.")

    async def broadcast(self, data: dict, room: str = "global") -> None:
        """Send JSON data to all clients in a room."""
        if room not in self._rooms:
            return
        dead: Set[WebSocket] = set()
        message = json.dumps(data)
        for ws in list(self._rooms[room]):
            try:
                await ws.send_text(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.disconnect(ws, room)

    def client_count(self, room: str = "global") -> int:
        return len(self._rooms.get(room, set()))

    def total_clients(self) -> int:
        return sum(len(v) for v in self._rooms.values())


# Singleton used across the app
manager = ConnectionManager()
