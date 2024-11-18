import hashlib
from typing import (
    Any,
    Dict,
    Optional,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request_cache import RequestCache


class RequestCacheService:

    @staticmethod
    def generate_request_hash(request_string: str) -> str:
        """Генерация хеша"""
        return hashlib.sha256(request_string.encode()).hexdigest()

    @staticmethod
    async def find_data_by_hash(session: AsyncSession, data_hash: str) -> Optional[str]:
        """Поиск записей по хешу"""
        # Ищем похожий запрос
        existent_cache = (
            await session.execute(
                select(RequestCache).where(RequestCache.hash == data_hash)
            )
        ).scalar_one_or_none()

        if existent_cache:
            return existent_cache.data

    @staticmethod
    async def create_request_hash(
        session: AsyncSession, data_hash: str, data: Dict[str, Any]
    ) -> RequestCache:
        """Создание новых записей в БД"""
        request_cache = RequestCache(hash=data_hash, data=data)
        session.add(request_cache)

        return request_cache
