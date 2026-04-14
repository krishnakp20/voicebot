from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class BillingUsage(Base, TimestampMixin):
    __tablename__ = "billing"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), index=True)
    month: Mapped[str] = mapped_column(String(7), index=True)
    call_minutes: Mapped[float] = mapped_column(Float, default=0)
    call_cost: Mapped[float] = mapped_column(Float, default=0)
    openai_tokens: Mapped[int] = mapped_column(Integer, default=0)
    openai_cost: Mapped[float] = mapped_column(Float, default=0)
    sarvam_seconds: Mapped[float] = mapped_column(Float, default=0)
    sarvam_cost: Mapped[float] = mapped_column(Float, default=0)
    total_cost: Mapped[float] = mapped_column(Float, default=0)
