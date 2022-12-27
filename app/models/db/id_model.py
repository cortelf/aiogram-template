from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4


class IdModel:
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
