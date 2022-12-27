from typing import Optional
from .interface.alchemy_uow import AlchemyUnitOfWork
from .interface.bot_uow import BaseBotUnitOfWork
from .repository.bot_user import BaseBotUserRepository, BotUserRepository


class BotUnitOfWork(BaseBotUnitOfWork, AlchemyUnitOfWork):
    _bot_users: Optional[BotUserRepository] = None

    @property
    def bot_users(self) -> BaseBotUserRepository:
        if self._bot_users is None:
            self._bot_users = BotUserRepository(self._session)
        return self._bot_users
