from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
)

from app.services.utils import get_snake_case

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, doc="Идентификатор объекта")

    @declared_attr
    def __tablename__(cls):
        return get_snake_case(cls.__name__)

    @declared_attr
    def __table_args__(cls):
        return {"comment": cls.__doc__.strip()}
