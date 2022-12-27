from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from internationalization import Internationalization
from internationalization.exceptions import LanguageNotPresentError


class I18nMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        i18n = Internationalization()
        try:
            lang = i18n.get_language(event.from_user.language_code)
        except LanguageNotPresentError:
            lang = i18n.get_language("en")
        data['i18n'] = i18n
        data['lang'] = lang
        return await handler(event, data)
