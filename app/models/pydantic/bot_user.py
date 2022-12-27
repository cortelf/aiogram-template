from datetime import datetime
from .id import PydanticIdModel


class BotUser(PydanticIdModel):
    telegram_id: int
    created_at: datetime
