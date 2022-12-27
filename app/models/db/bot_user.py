from .base import Base
from sqlalchemy import BigInteger, Integer, DateTime, Uuid, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .id_model import IdModel
from datetime import datetime


class BotUserModel(Base, IdModel):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
