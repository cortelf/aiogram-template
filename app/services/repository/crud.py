from typing import TypeVar, Generic, List, Type
from uuid import UUID

from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.db.id_model import IdModel
from models.pydantic.id import PydanticIdModel
from services.repository.interface.alchemy import AlchemyRepository
from .helpers import return_one
from .interface.crud import DomainModelType, BaseCRUDRepository

DbModelType = TypeVar("DbModelType", bound=IdModel)


class CRUDRepository(Generic[DbModelType, DomainModelType], BaseCRUDRepository[DomainModelType], AlchemyRepository):
    def __init__(self, session: AsyncSession, domain_type: Type[PydanticIdModel], db_type: Type[IdModel]):
        super().__init__(domain_type)
        AlchemyRepository.__init__(self, session)
        self.db_type = db_type

    async def find_by_id(self, id_: UUID) -> DomainModelType:
        db_obj = await self.session.scalars(select(self.db_type).where(self.db_type.id == id_))
        return self.domain_type.from_orm(return_one(db_obj.all()))

    async def create(self, model: DomainModelType) -> DomainModelType:
        db_obj = await self.session.scalar(insert(self.db_type).returning(self.db_type), model.dict())
        return self.domain_type.from_orm(db_obj)

    async def update(self, model: DomainModelType):
        await self.session.execute(update(self.db_type).where(self.db_type.id == model.id).values(**model.dict()))

    async def read(self) -> List[DomainModelType]:
        db_obj = await self.session.scalars(select(self.db_type))
        return [self.domain_type.from_orm(x) for x in db_obj.all()]

    async def delete(self, model: DomainModelType):
        await self.session.execute(delete(self.db_type).where(self.db_type.id == model.id))
