from app.models.base import Base
from sqlalchemy.orm import mapped_column , Mapped
from uuid import uuid4


class CategoryORM(Base):
    __tablename__ = 'categories'

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)