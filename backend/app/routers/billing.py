from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.billing import BillingUsage
from app.models.user import User

router = APIRouter()


@router.get("")
def get_billing(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[dict]:
    month = datetime.utcnow().strftime("%Y-%m")
    stmt = select(BillingUsage).where(BillingUsage.month == month)
    if user.role != "admin":
        stmt = stmt.where(BillingUsage.client_id == user.client_id)
    rows = db.scalars(stmt).all()
    return [
        {
            "month": row.month,
            "client_id": row.client_id,
            "call_minutes": row.call_minutes,
            "call_cost": row.call_cost,
            "openai_tokens": row.openai_tokens,
            "openai_cost": row.openai_cost,
            "sarvam_seconds": row.sarvam_seconds,
            "sarvam_cost": row.sarvam_cost,
            "total_cost": row.total_cost,
        }
        for row in rows
    ]
