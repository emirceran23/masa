"""WebSocket endpoint for real-time analysis progress."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.websocket_manager import ws_manager

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/{contract_id}")
async def websocket_progress(websocket: WebSocket, contract_id: str):
    """Clients connect here to receive real-time analysis updates."""
    await ws_manager.connect(contract_id, websocket)
    try:
        while True:
            # Keep connection alive — wait for client messages (ping/pong)
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(contract_id, websocket)
