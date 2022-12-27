from abc import ABC
from typing import Callable

from services.unit_of_work import BaseBotUnitOfWork


class UoWService(ABC):
    uow_factory: Callable[[], BaseBotUnitOfWork]

    def __init__(self, bot_uow: Callable[[], BaseBotUnitOfWork]):
        self.uow_factory = bot_uow
