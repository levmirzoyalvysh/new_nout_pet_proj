
from uuid import uuid4
from sqlalchemy.orm import mapped_column,DeclarativeBase , Mapped



class Base(DeclarativeBase):

    id : Mapped[str] = mapped_column(primary_key=True,default=lambda: str(uuid4()))