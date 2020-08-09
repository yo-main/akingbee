import uuid

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator

class UUID(TypeDecorator):
    # pylint: disable=unused-argument, no-self-use
    impl = BINARY(16)

    def process_bind_params(self, value, dialect):
        try:
            converted = uuid.UUID(value)
        except:
            raise ValueError(f"{value=} - not a valid UUID")

        return converted.bytes

    def process_result_value(self, value, dialect):
        if not value:
            return None

        return uuid.UUID(bytes=value)

    def python_type(self):
        return uuid.UUID


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

Base = declarative_base()
Base.metadata = MetaData(naming_convention=convention)
