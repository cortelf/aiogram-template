from abc import ABC, abstractmethod

from aiogram import Router


class Controller(ABC):
    @abstractmethod
    def register(self, router: Router):
        pass
