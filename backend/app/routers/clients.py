import secrets

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import admin_only, get_db
from app.core.security import hash_password
from app.models.client import Client
from app.models.user import User
from app.schemas.client import ClientCreate, ClientOut
from app.services.audit import write_audit

router = APIRouter()


@router.post("", response_model=ClientOut)
def create_client(
    payload: ClientCreate, db: Session = Depends(get_db), admin: User = Depends(admin_only)
) -> Client:
    exists = db.scalar(select(Client).where(Client.name == payload.name))
    if exists:
        raise HTTPException(status_code=400, detail="Client name already exists")

    client = Client(name=payload.name, plan=payload.plan, api_key=secrets.token_urlsafe(32), is_enabled=True)
    db.add(client)
    db.flush()
    client.client_id = client.id

    client_user = User(
        client_id=client.id,
        email=payload.admin_email,
        full_name=payload.admin_name,
        password_hash=hash_password(payload.admin_password),
        role="client",
    )
    db.add(client_user)
    db.commit()
    db.refresh(client)

    write_audit(
        db,
        admin,
        action="client_created",
        target_type="client",
        target_id=str(client.id),
        detail=f"Created client {client.name}",
        client_id=client.id,
    )
    return client


@router.get("", response_model=list[ClientOut])
def list_clients(
    enabled: bool | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
) -> list[Client]:
    stmt = select(Client)
    if enabled is not None:
        stmt = stmt.where(Client.is_enabled == enabled)
    return list(db.scalars(stmt).all())


@router.patch("/{client_id}/status", response_model=ClientOut)
def update_client_status(
    client_id: int, enabled: bool, db: Session = Depends(get_db), admin: User = Depends(admin_only)
) -> Client:
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client.is_enabled = enabled
    db.commit()
    db.refresh(client)
    write_audit(
        db,
        admin,
        action="client_status_updated",
        target_type="client",
        target_id=str(client_id),
        detail=f"Client enabled={enabled}",
        client_id=client_id,
    )
    return client
