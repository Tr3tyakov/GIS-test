from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import ROUTERS
from app.config import settings
from app.core.context import ApplicationContext
from app.core.database import Database


class Application:
    def __init__(self) -> None:
        self.app = FastAPI(
            lifespan=self.lifespan,
        )
        self.database = Database(settings=settings.POSTGRES)

        self.context = self._init_context()

    @asynccontextmanager
    async def lifespan(self, _):
        self.database._connect()
        yield
        await self.database._close()

    def _init_context(self) -> ApplicationContext:
        """Инициализация контекста сервиса"""
        return ApplicationContext(
            database=self.database,
        )

    def _add_middlewares(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:3000",
                "http://localhost:3001",
                "http://localhost:3002",
            ],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            allow_headers=["*"],
        )

    def _init_logger(self) -> None:
        """Инициализация логгера"""
        dictConfig(settings.LOGGING)

    def _add_routers(self) -> None:
        """Добавление роутеров"""
        for router in ROUTERS:
            self.app.include_router(router)

    def init_app(self) -> FastAPI:
        """Инициализация зависимостей"""
        self._init_logger()
        self._add_middlewares()
        self._add_routers()
        self.app.extra["context"] = self._init_context()
        return self.app


app = Application().init_app()
