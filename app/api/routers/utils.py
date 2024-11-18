import logging

from fastapi import (
    APIRouter,
    Depends,
    Request,
)


class LoggingRouter(APIRouter):
    """Класс роутера с логированием"""

    async def log_request(self, request: Request) -> None:
        logging.info("Инициализирован %s запрос на %s", request.method, request.url)

    def add_api_route(self, *args, **kwargs) -> None:
        kwargs["dependencies"] = [Depends(self.log_request)]
        super().add_api_route(*args, **kwargs)
