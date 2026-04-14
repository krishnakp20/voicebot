from fastapi import APIRouter, Depends
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.agent import Agent
from app.models.call import Call
from app.models.billing import BillingUsage
from app.models.user import User

router = APIRouter()


@router.get("/stats")
def dashboard_stats(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    calls_stmt = select(
        func.count(Call.id),
        func.sum(Call.duration),
        func.sum(case((Call.status == "completed", 1), else_=0)),
    )
    agent_stmt = select(func.count(Agent.id))
    billing_stmt = select(func.sum(BillingUsage.total_cost))

    if user.role != "admin":
        calls_stmt = calls_stmt.where(Call.client_id == user.client_id)
        agent_stmt = agent_stmt.where(Agent.client_id == user.client_id)
        billing_stmt = billing_stmt.where(BillingUsage.client_id == user.client_id)

    total_calls, total_duration, success_calls = db.execute(calls_stmt).one()
    active_agents = db.scalar(agent_stmt) or 0
    total_cost = db.scalar(billing_stmt) or 0.0
    success_rate = (success_calls / total_calls * 100) if total_calls else 0

    return {
        "total_calls": total_calls or 0,
        "total_duration": total_duration or 0,
        "active_agents": active_agents,
        "call_success_rate": round(success_rate, 2),
        "cost_usage": round(float(total_cost), 2),
    }
