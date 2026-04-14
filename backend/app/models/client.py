from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, default=0, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    plan: Mapped[str] = mapped_column(String(50), default="starter")
    api_key: Mapped[str] = mapped_column(String(128), unique=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    users = relationship("User", back_populates="client")
    agents = relationship("Agent", back_populates="client")
