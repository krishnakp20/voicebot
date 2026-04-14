from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Agent(Base, TimestampMixin):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), index=True)
    agent_name: Mapped[str] = mapped_column(String(120), index=True)
    prompt: Mapped[str] = mapped_column(Text)
    welcome_message: Mapped[str] = mapped_column(Text)
    voice: Mapped[str] = mapped_column(String(80))
    language: Mapped[str] = mapped_column(String(20), default="en")

    client = relationship("Client", back_populates="agents")
