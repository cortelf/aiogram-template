from aiogram.filters import Filter
from aiogram.types import Message
from internationalization import Internationalization


class I18nPhraseFilter(Filter):
    def __init__(self, text: str) -> None:
        self.text = text

    async def __call__(self, message: Message, i18n: Internationalization) -> bool:
        return message.text == self.text or \
            any(filter(lambda x: x == message.text, Internationalization().find_phrase(self.text)))
