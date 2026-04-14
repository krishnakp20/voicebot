from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str
    plan: str = "starter"
    admin_email: str
    admin_name: str
    admin_password: str


class ClientOut(BaseModel):
    id: int
    name: str
    plan: str
    api_key: str
    is_enabled: bool

    class Config:
        from_attributes = True
