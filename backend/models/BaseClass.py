import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.dialects.postgresql import UUID


@as_declarative()
class Base:
    __abstract__ = True
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BareBaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)