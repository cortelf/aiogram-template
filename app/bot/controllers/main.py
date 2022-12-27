from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from internationalization import Language

from models.pydantic.bot_user import BotUser
from .interface.controller import Controller


class MainController(Controller):
    async def on_start(self, message: Message, lang: Language, user: BotUser):
        await message.answer(lang.hello.format(user_uuid=user.id))

    def register(self, router: Router):
        router.message.register(self.on_start, Command("start"))
