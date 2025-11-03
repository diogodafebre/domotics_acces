"""WebSocket router."""
import json
import logging
from typing import Dict, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from app.security.tokens import decode_access_token

router = APIRouter(tags=["WebSocket"])

logger = logging.getLogger(__name__)

# Active WebSocket connections
active_connections: Set[WebSocket] = set()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication.

    Requires access token in query parameter: /ws?token=<access_token>

    Supported messages:
    - {"type": "echo", "payload": "..."} - Echo back the payload
    """
    # Get token from query params
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing token")
        return

    # Validate token
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        return

    email = payload.get("sub")
    if not email:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        return

    # Accept connection
    await websocket.accept()
    active_connections.add(websocket)

    logger.info(f"WebSocket connection established for user: {email}")

    # Send welcome message
    await websocket.send_json({"type": "welcome", "message": f"Welcome {email}!"})

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()

            try:
                message: Dict = json.loads(data)
                msg_type = message.get("type")

                if msg_type == "echo":
                    # Echo back the payload
                    payload_data = message.get("payload", "")
                    await websocket.send_json(
                        {"type": "echo", "payload": payload_data, "from": "server"}
                    )
                elif msg_type == "ping":
                    # Respond to ping with pong
                    await websocket.send_json({"type": "pong"})
                else:
                    # Unknown message type
                    await websocket.send_json(
                        {"type": "error", "message": f"Unknown message type: {msg_type}"}
                    )

            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user: {email}")
        active_connections.discard(websocket)
    except Exception as e:
        logger.error(f"WebSocket error for user {email}: {e}")
        active_connections.discard(websocket)
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
