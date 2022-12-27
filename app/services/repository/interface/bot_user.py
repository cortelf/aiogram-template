from abc import abstractmethod, ABC

from models.pydantic.bot_user import BotUser
from .crud import BaseCRUDRepository


class BaseBotUserRepository(BaseCRUDRepository[BotUser], ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> BotUser:
        pass
