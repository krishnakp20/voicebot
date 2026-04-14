from pydantic import BaseModel


class AgentCreate(BaseModel):
    agent_name: str
    prompt: str
    welcome_message: str
    voice: str
    language: str = "en"


class AgentUpdate(BaseModel):
    agent_name: str | None = None
    prompt: str | None = None
    welcome_message: str | None = None
    voice: str | None = None
    language: str | None = None


class AgentOut(BaseModel):
    id: int
    client_id: int
    agent_name: str
    prompt: str
    welcome_message: str
    voice: str
    language: str

    class Config:
        from_attributes = True
