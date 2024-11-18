from dataclasses import dataclass
from typing import Optional

from fastapi import Request

from app.core.database import Database


@dataclass
class ApplicationContext:
    """Контекст сервиса"""

    database: Optional[Database] = None

    @staticmethod
    def get_context(request: Request) -> "ApplicationContext":
        return request.app.extra["context"]
