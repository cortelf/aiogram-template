import uuid
from datetime import datetime
from typing import Callable

from models.pydantic.bot_user import BotUser
from .interface.uow_service import UoWService
from .interface.auth_service import BaseAuthService
from .unit_of_work import BaseBotUnitOfWork
from .repository.exceptions.not_found import NotFoundException


class AuthService(BaseAuthService, UoWService):
    def __init__(self, bot_uow: Callable[[], BaseBotUnitOfWork]):
        UoWService.__init__(self, bot_uow)

    async def auth_telegram_user(self, telegram_id: int) -> BotUser:
        async with self.uow_factory() as uow:
            try:
                return await uow.bot_users.get_by_telegram_id(telegram_id)
            except NotFoundException:
                user = BotUser(
                    id=uuid.uuid4(),
                    created_at=datetime.utcnow(),
                    telegram_id=telegram_id
                )
                await uow.bot_users.create(user)
                await uow.commit()

                return user