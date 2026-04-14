from pydantic import BaseModel, field_validator


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("Invalid email format")
        return value


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    client_id: int
