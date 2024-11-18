from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from app.models.base import BaseModel


class CoordinateReferenceSystem(BaseModel):
    """
    Система координат
    """

    srid = Column(
        Integer, nullable=False, doc="Целочисленный идентификатор системы координат SRS"
    )
    name = Column(Text, nullable=True, doc="Название системы координат")
