import uuid

from app.core.config import settings


def create_room_for_call(client_id: int, agent_id: int) -> dict[str, str]:
    room_name = f"tenant-{client_id}-agent-{agent_id}-{uuid.uuid4().hex[:8]}"
    return {
        "room_name": room_name,
        "ws_url": settings.livekit_ws_url,
        "api_key": settings.livekit_api_key,
    }
