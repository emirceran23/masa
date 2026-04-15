"""WebSocket connection manager for real-time progress updates."""

from __future__ import annotations

import json
from fastapi import WebSocket


class WebSocketManager:
    """Manages active WebSocket connections per contract analysis."""

    def __init__(self) -> None:
        # contract_id → list of connected websockets
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, contract_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self._connections.setdefault(contract_id, []).append(ws)

    def disconnect(self, contract_id: str, ws: WebSocket) -> None:
        conns = self._connections.get(contract_id, [])
        if ws in conns:
            conns.remove(ws)
        if not conns:
            self._connections.pop(contract_id, None)

    async def broadcast(self, contract_id: str, message: dict) -> None:
        """Send a JSON message to every client watching a given contract."""
        conns = self._connections.get(contract_id, [])
        dead: list[WebSocket] = []
        for ws in conns:
            try:
                await ws.send_text(json.dumps(message, ensure_ascii=False))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(contract_id, ws)

    async def send_progress(
        self,
        contract_id: str,
        step: str,
        progress: int,
        message: str,
    ) -> None:
        await self.broadcast(
            contract_id,
            {
                "type": "progress",
                "step": step,
                "progress": progress,
                "message": message,
            },
        )


ws_manager = WebSocketManager()
