from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.billing import BillingUsage
from app.models.call import Call

CALL_COST_PER_MIN = 0.08
OPENAI_COST_PER_1K_TOKENS = 0.002
SARVAM_COST_PER_MIN = 0.05


def upsert_monthly_usage(db: Session, call: Call, openai_tokens: int = 0, sarvam_seconds: int = 0) -> None:
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    row = db.scalar(
        select(BillingUsage).where(BillingUsage.client_id == call.client_id, BillingUsage.month == month)
    )
    if not row:
        row = BillingUsage(client_id=call.client_id, month=month)
        db.add(row)
        db.flush()

    call_minutes = call.duration / 60
    row.call_minutes += call_minutes
    row.call_cost += round(call_minutes * CALL_COST_PER_MIN, 4)
    row.openai_tokens += openai_tokens
    row.openai_cost += round((openai_tokens / 1000) * OPENAI_COST_PER_1K_TOKENS, 4)
    row.sarvam_seconds += sarvam_seconds
    row.sarvam_cost += round((sarvam_seconds / 60) * SARVAM_COST_PER_MIN, 4)
    row.total_cost = round(row.call_cost + row.openai_cost + row.sarvam_cost, 4)
