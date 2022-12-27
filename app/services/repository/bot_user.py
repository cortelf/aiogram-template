from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.db.bot_user import BotUserModel
from abc import ABC, abstractmethod

from models.pydantic.bot_user import BotUser
from .helpers import return_one
from .crud import BaseCRUDRepository, CRUDRepository


class BaseBotUserRepository(BaseCRUDRepository[BotUser], ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> BotUser:
        pass


class BotUserRepository(CRUDRepository[BotUser, BotUserModel], BaseBotUserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            db_type=BotUserModel,
            domain_type=BotUser
        )

    async def get_by_telegram_id(self, telegram_id: int) -> BotUser:
        db_obj = await self.session.scalars(select(self.db_type).where(self.db_type.telegram_id == telegram_id))
        return self.domain_type.from_orm(return_one(db_obj.all()))
