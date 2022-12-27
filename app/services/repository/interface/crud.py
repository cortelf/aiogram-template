from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Sequence, Type
from uuid import UUID

from models.pydantic.id import PydanticIdModel

DomainModelType = TypeVar("DomainModelType", bound=PydanticIdModel)


class BaseCRUDRepository(Generic[DomainModelType], ABC):

    def __init__(self, domain_type: Type[PydanticIdModel]):
        self.domain_type = domain_type

    @abstractmethod
    async def create(self, model: DomainModelType) -> DomainModelType:
        pass

    @abstractmethod
    async def update(self, model: DomainModelType):
        pass

    @abstractmethod
    async def read(self) -> Sequence[DomainModelType]:
        pass

    @abstractmethod
    async def delete(self, model: DomainModelType):
        pass

    @abstractmethod
    async def find_by_id(self, id_: UUID) -> DomainModelType:
        pass