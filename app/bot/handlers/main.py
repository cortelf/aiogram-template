from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from internationalization import Language

from models.db import BotUser


async def on_start(message: Message, lang: Language, user: BotUser):
    await message.answer(lang.hello.format(user_uuid=user.id))


def register_main_routes(router: Router):
    router.message.register(on_start, Command("start"))
