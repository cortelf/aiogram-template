from uuid import UUID
from pydantic import BaseModel


class BaseIdModel(BaseModel):
    id: UUID

    class Config:
        orm_mode = True
