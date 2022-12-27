from uuid import UUID
from pydantic import BaseModel


class PydanticIdModel(BaseModel):
    id: UUID

    class Config:
        orm_mode = True
