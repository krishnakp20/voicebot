from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class Call(Base, TimestampMixin):
    __tablename__ = "calls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), index=True)
    agent_id: Mapped[int] = mapped_column(Integer, ForeignKey("agents.id"), index=True)
    call_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(40))
    customer_name: Mapped[str] = mapped_column(String(120))
    room_name: Mapped[str] = mapped_column(String(120))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(40), default="queued")
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    recording_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    extracted_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
