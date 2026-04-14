from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.client import Client
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.role == "client":
        client = db.get(Client, user.client_id)
        if not client or not client.is_enabled:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Client disabled")
    token = create_access_token({"sub": str(user.id), "role": user.role, "client_id": user.client_id})
    return TokenResponse(access_token=token, role=user.role, client_id=user.client_id)


@router.post("/bootstrap-admin")
def bootstrap_admin(db: Session = Depends(get_db)) -> dict[str, str]:
    existing_admin = db.scalar(select(User).where(User.role == "admin"))
    if existing_admin:
        return {"message": "Admin already exists"}

    root_client = Client(name="system", plan="internal", api_key="system", is_enabled=True, client_id=0)
    db.add(root_client)
    db.flush()

    admin = User(
        client_id=root_client.id,
        email="admin@voicebot.local",
        full_name="Platform Admin",
        password_hash=hash_password("Admin@123"),
        role="admin",
        is_active=True,
    )
    db.add(admin)
    db.commit()
    return {"message": "Admin seeded: admin@voicebot.local / Admin@123"}
