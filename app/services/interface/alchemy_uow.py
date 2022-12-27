from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .base_uow import BaseUnitOfWork


class AlchemyUnitOfWork(BaseUnitOfWork, ABC):
    _session: AsyncSession

    def __init__(self, factory: async_sessionmaker):
        self._session = factory()

    async def __aenter__(self):
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
