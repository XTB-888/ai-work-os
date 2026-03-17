"""
WebSocket endpoint for real-time project updates.
"""
import json
import asyncio
from uuid import UUID
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections per project."""

    def __init__(self):
        self._connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, project_id: str, ws: WebSocket):
        await ws.accept()
        self._connections.setdefault(project_id, set()).add(ws)

    def disconnect(self, project_id: str, ws: WebSocket):
        conns = self._connections.get(project_id)
        if conns:
            conns.discard(ws)

    async def broadcast(self, project_id: str, event: str, data: dict):
        """Send an event to every client watching a project."""
        payload = json.dumps({"event": event, "data": data}, default=str)
        conns = self._connections.get(project_id, set()).copy()
        for ws in conns:
            try:
                await ws.send_text(payload)
            except Exception:
                self.disconnect(project_id, ws)


manager = ConnectionManager()


@router.websocket("/projects/{project_id}")
async def project_ws(websocket: WebSocket, project_id: str):
    await manager.connect(project_id, websocket)
    try:
        while True:
            # keep connection alive; client can send pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(project_id, websocket)
