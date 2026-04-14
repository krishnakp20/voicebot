from sqlalchemy import ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class Transcript(Base, TimestampMixin):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), index=True)
    call_id: Mapped[str] = mapped_column(String(80), index=True)
    content: Mapped[str] = mapped_column(Text)
    extracted_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
