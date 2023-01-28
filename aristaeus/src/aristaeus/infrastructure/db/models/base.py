import re
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column


class BaseModel(DeclarativeBase):

    id: Mapped[int] = mapped_column(primary_key=True)

    date_creation: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    date_modification: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        tablename = cls.__name__[:-5] if cls.__name__.endswith("Model") else cls.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", tablename).lower()

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
