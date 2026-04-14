from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.agent import Agent
from app.models.user import User
from app.schemas.agent import AgentCreate, AgentOut, AgentUpdate
from app.services.audit import write_audit

router = APIRouter()


@router.post("", response_model=AgentOut)
def create_agent(
    payload: AgentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Agent:
    client_id = user.client_id
    agent = Agent(client_id=client_id, **payload.model_dump())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    write_audit(
        db, user, "agent_created", "agent", str(agent.id), f"Created agent {agent.agent_name}", client_id=client_id
    )
    return agent


@router.get("", response_model=list[AgentOut])
def list_agents(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[Agent]:
    stmt = select(Agent)
    if user.role != "admin":
        stmt = stmt.where(Agent.client_id == user.client_id)
    return list(db.scalars(stmt).all())


@router.put("/{agent_id}", response_model=AgentOut)
def update_agent(
    agent_id: int,
    payload: AgentUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Agent:
    agent = db.get(Agent, agent_id)
    if not agent or (user.role != "admin" and agent.client_id != user.client_id):
        raise HTTPException(status_code=404, detail="Agent not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(agent, field, value)
    db.commit()
    db.refresh(agent)
    write_audit(
        db, user, "agent_updated", "agent", str(agent.id), f"Updated agent {agent.agent_name}", client_id=agent.client_id
    )
    return agent


@router.delete("/{agent_id}")
def delete_agent(
    agent_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict[str, str]:
    agent = db.get(Agent, agent_id)
    if not agent or (user.role != "admin" and agent.client_id != user.client_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    write_audit(db, user, "agent_deleted", "agent", str(agent_id), "Deleted agent", client_id=agent.client_id)
    return {"message": "Agent deleted"}
