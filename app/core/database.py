import logging
from contextlib import asynccontextmanager

from dynaconf.utils.boxing import DynaBox
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.config import DB_URL
from app.interfaces.database import IDatabase


class Database(IDatabase):
    def __init__(self, settings: DynaBox) -> None:
        self.settings = settings
        self._async_engine = None
        self._async_session = None

    def _connect(self) -> None:
        """
        Инициализация подключения к базе данных
        """

        logging.info("Инициализировано подключение к базе данных")
        self._async_engine = create_async_engine(url=DB_URL)
        self._async_session = sessionmaker(
            self._async_engine,
            expire_on_commit=False,
            autoflush=True,
            autocommit=False,
            class_=AsyncSession,
        )

    @asynccontextmanager
    async def _session(self):
        """
        Контекстный менеджер сессии
        """

        async_session = self._async_session()
        try:
            yield async_session
            await async_session.commit()
        except Exception as exc:
            await async_session.rollback()
            logging.exception("Ошибка сессии: %s", str(exc))
            raise exc
        finally:
            await async_session.close()

    async def _close(self) -> None:
        """
        Закрытие подключения к базе данных
        """

        logging.info("Закрытие подключения к базе данных")
        if self._async_engine:
            await self._async_engine.dispose()


class DatabaseException(Exception):
    pass
