from datetime import datetime
from .id import BaseIdModel


class BotUser(BaseIdModel):
    telegram_id: int
    created_at: datetime
