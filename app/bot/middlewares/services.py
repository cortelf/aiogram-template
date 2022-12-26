from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from services.auth import BaseAuthService


class ServicesMiddleware(BaseMiddleware):
    auth: BaseAuthService
    bot: Bot

    def __init__(self, auth: BaseAuthService, bot: Bot) -> None:
        self.auth = auth
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data['auth'] = self.auth
        data["bot"] = self.bot
        return await handler(event, data)
    