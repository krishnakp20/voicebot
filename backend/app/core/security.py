from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256

from app.core.config import settings

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        if hashed_password.startswith("$pbkdf2-sha256$"):
            return pbkdf2_sha256.verify(password, hashed_password)
        if hashed_password.startswith("$2"):
            raw = password.encode("utf-8")
            if len(raw) > 72:
                return False
            return bcrypt.checkpw(raw, hashed_password.encode("utf-8"))
        return False
    except Exception:
        return False


def create_access_token(data: dict[str, Any], expires_minutes: int | None = None) -> str:
    expires_delta = timedelta(minutes=expires_minutes or settings.jwt_expire_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None
