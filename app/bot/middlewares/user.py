from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from services.auth import BaseAuthService


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        auth_service: BaseAuthService = data['auth']
        data['user'] = await auth_service.auth_telegram_user(event.from_user.id)
        return await handler(event, data)
