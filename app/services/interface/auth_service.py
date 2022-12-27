from abc import abstractmethod, ABC

from models.pydantic.bot_user import BotUser


class BaseAuthService(ABC):
    @abstractmethod
    async def auth_telegram_user(self, telegram_id: int) -> BotUser:
        pass
