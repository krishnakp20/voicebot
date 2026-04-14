from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.user import User


def write_audit(
    db: Session,
    user: User,
    action: str,
    target_type: str,
    target_id: str,
    detail: str,
    client_id: int | None = None,
) -> None:
    row = AuditLog(
        client_id=client_id if client_id is not None else user.client_id,
        user_id=user.id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail=detail,
    )
    db.add(row)
    db.commit()
