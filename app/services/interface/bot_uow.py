from abc import ABC, abstractmethod

from .base_uow import BaseUnitOfWork
from ..repository.bot_user import BaseBotUserRepository


class BaseBotUnitOfWork(BaseUnitOfWork, ABC):
    @property
    @abstractmethod
    def bot_users(self) -> BaseBotUserRepository:
        pass
