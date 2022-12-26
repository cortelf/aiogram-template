from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from .repository.bot_user import BaseBotUserRepository, BotUserRepository


class BaseUnitOfWork(ABC):
    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    async def __aenter__(self) -> 'BaseUnitOfWork':
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class AlchemyUnitOfWork(BaseUnitOfWork, ABC):
    _session: AsyncSession

    def __init__(self, factory: async_sessionmaker):
        self._session = factory()

    async def __aenter__(self):
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()


class BaseBotUnitOfWork(BaseUnitOfWork, ABC):
    @property
    @abstractmethod
    def bot_users(self) -> BaseBotUserRepository:
        pass


class BotUnitOfWork(BaseBotUnitOfWork, AlchemyUnitOfWork):
    _bot_users: Optional[BotUserRepository] = None

    @property
    def bot_users(self) -> BaseBotUserRepository:
        if self._bot_users is None:
            self._bot_users = BotUserRepository(self._session)
        return self._bot_users
