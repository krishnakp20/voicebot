from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.agent import Agent
from app.models.call import Call
from app.models.transcript import Transcript
from app.models.user import User
from app.schemas.call import CallOut, CallStartRequest, CallTransferRequest
from app.services.audit import write_audit
from app.services.billing import upsert_monthly_usage
from app.services.livekit_service import create_room_for_call
from app.services.llm_service import extract_structured_data
from app.services.queue import enqueue_call_job
from app.services.storage import stream_recording_target

router = APIRouter()


@router.post("/start")
def start_call(
    payload: CallStartRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict:
    agent = db.get(Agent, payload.agent_id)
    if not agent or (user.role != "admin" and agent.client_id != user.client_id):
        raise HTTPException(status_code=404, detail="Agent not found")

    livekit_data = create_room_for_call(agent.client_id, agent.id)
    call_ref = f"CALL-{uuid4().hex[:12].upper()}"
    row = Call(
        call_id=call_ref,
        client_id=agent.client_id,
        agent_id=agent.id,
        phone_number=payload.phone_number,
        customer_name=payload.customer_name,
        room_name=livekit_data["room_name"],
        start_time=datetime.now(timezone.utc),
        status="initiated",
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    enqueue_call_job(
        {
            "call_id": row.call_id,
            "client_id": row.client_id,
            "agent_id": row.agent_id,
            "prompt": agent.prompt,
            "voice": agent.voice,
            "customer_name": payload.customer_name,
            "phone_number": payload.phone_number,
        }
    )
    return {
        "call_id": row.call_id,
        "room_name": row.room_name,
        "livekit_ws": livekit_data["ws_url"],
        "agent_metadata": {
            "client_id": row.client_id,
            "agent_id": row.agent_id,
            "prompt": agent.prompt,
            "voice": agent.voice,
            "customer_name": row.customer_name,
        },
    }


@router.get("", response_model=list[CallOut])
def list_calls(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[Call]:
    stmt = select(Call)
    if user.role != "admin":
        stmt = stmt.where(Call.client_id == user.client_id)
    return list(db.scalars(stmt.order_by(Call.created_at.desc())).all())


@router.get("/{call_id}", response_model=CallOut)
def get_call(call_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Call:
    row = db.scalar(select(Call).where(Call.call_id == call_id))
    if not row or (user.role != "admin" and row.client_id != user.client_id):
        raise HTTPException(status_code=404, detail="Call not found")
    return row


@router.post("/{call_id}/transfer")
def transfer_call(
    call_id: str,
    payload: CallTransferRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict[str, str]:
    row = db.scalar(select(Call).where(Call.call_id == call_id))
    if not row or (user.role != "admin" and row.client_id != user.client_id):
        raise HTTPException(status_code=404, detail="Call not found")
    row.status = f"transferred:{payload.target_type}"
    db.commit()
    write_audit(db, user, "call_transferred", "call", row.call_id, f"Transfer {payload.target_type}", row.client_id)
    return {"message": "Transfer initiated"}


@router.get("/{call_id}/recording")
def fetch_recording(call_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = db.scalar(select(Call).where(Call.call_id == call_id))
    if not row or (user.role != "admin" and row.client_id != user.client_id):
        raise HTTPException(status_code=404, detail="Call not found")
    if not row.recording_url:
        raise HTTPException(status_code=404, detail="Recording unavailable")

    target = stream_recording_target(row.recording_url)
    if target.startswith("http") or target.startswith("s3://"):
        return {"recording_url": target}
    if not Path(target).exists():
        raise HTTPException(status_code=404, detail="Recording file missing")
    return FileResponse(target, media_type="audio/mpeg", filename=f"{call_id}.mp3")


@router.post("/events/finalize/{call_id}")
async def finalize_call_from_agent(
    call_id: str,
    body: dict,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    row = db.scalar(select(Call).where(Call.call_id == call_id))
    if not row:
        raise HTTPException(status_code=404, detail="Call not found")
    row.end_time = datetime.now(timezone.utc)
    row.duration = body.get("duration", 0)
    row.status = body.get("status", "completed")
    row.transcript = body.get("transcript")
    row.recording_url = body.get("recording_url")
    row.extracted_data = await extract_structured_data(body.get("transcript", ""))
    upsert_monthly_usage(
        db,
        row,
        openai_tokens=body.get("openai_tokens", 0),
        sarvam_seconds=body.get("sarvam_seconds", 0),
    )

    transcript = Transcript(
        client_id=row.client_id,
        call_id=row.call_id,
        content=row.transcript or "",
        extracted_json=row.extracted_data,
    )
    db.add(transcript)
    db.commit()
    return {"message": "Call finalized"}
