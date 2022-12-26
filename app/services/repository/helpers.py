from typing import TypeVar, Sequence
from .exceptions.not_found import NotFoundException

T = TypeVar("T")


def return_one(source: Sequence[T]) -> T:
    if len(source) == 0:
        raise NotFoundException()
    return source[0]
