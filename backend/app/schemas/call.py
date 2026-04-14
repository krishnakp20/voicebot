from datetime import datetime

from pydantic import BaseModel


class CallStartRequest(BaseModel):
    agent_id: int
    phone_number: str
    customer_name: str


class CallTransferRequest(BaseModel):
    target_type: str
    target_agent_id: int | None = None
    human_agent: str | None = None


class CallOut(BaseModel):
    id: int
    call_id: str
    client_id: int
    agent_id: int
    phone_number: str
    start_time: datetime
    end_time: datetime | None
    duration: int
    status: str
    transcript: str | None
    recording_url: str | None

    class Config:
        from_attributes = True
