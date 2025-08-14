from datetime import datetime
from sqlalchemy import BigInteger, String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class PostType:
    LOAD = "load"
    TRUCK = "truck"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    type: Mapped[str] = mapped_column(String(16), index=True)

    # Поля
    region_from: Mapped[str] = mapped_column(String(64))
    region_to: Mapped[str] = mapped_column(String(64))
    vehicle: Mapped[str] = mapped_column(String(64), default="")
    capacity: Mapped[str] = mapped_column(String(32), default="")
    cargo: Mapped[str] = mapped_column(String(64), default="")
    price: Mapped[str] = mapped_column(String(64), default="договорная")
    phone: Mapped[str] = mapped_column(String(64))
    note: Mapped[str] = mapped_column(Text, default="")
    hashtags: Mapped[str] = mapped_column(String(255), default="")

    # Служебные
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    message_id: Mapped[int | None] = mapped_column(Integer, default=None)
