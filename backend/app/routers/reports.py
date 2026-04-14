from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.call import Call
from app.models.user import User

router = APIRouter()


@router.get("")
def get_reports(
    from_date: datetime = Query(...),
    to_date: datetime = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    base = select(
        Call.agent_id,
        func.count(Call.id).label("calls"),
        func.sum(Call.duration).label("duration"),
    ).where(Call.start_time >= from_date, Call.start_time <= to_date)

    if user.role != "admin":
        base = base.where(Call.client_id == user.client_id)
    base = base.group_by(Call.agent_id)
    agent_rows = db.execute(base).all()

    total_stmt = select(func.count(Call.id), func.sum(Call.duration)).where(
        Call.start_time >= from_date, Call.start_time <= to_date
    )
    if user.role != "admin":
        total_stmt = total_stmt.where(Call.client_id == user.client_id)

    total_calls, total_duration = db.execute(total_stmt).one()
    return {
        "total_calls": total_calls or 0,
        "total_duration": total_duration or 0,
        "agent_performance": [
            {"agent_id": r.agent_id, "calls": r.calls or 0, "duration": r.duration or 0}
            for r in agent_rows
        ],
    }
