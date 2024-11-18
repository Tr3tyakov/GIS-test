from geoalchemy2 import Geometry
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Column,
    String,
    text,
)

from app.models.base import BaseModel


class RequestCache(BaseModel):
    """
    Кешированные данные запроса
    """

    hash = Column(String(256), unique=True, nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
