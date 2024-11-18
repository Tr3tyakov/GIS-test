import asyncio
from typing import (
    Any,
)

from fastapi import Depends
from geoalchemy2 import Geometry
from geoalchemy2 import functions as func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.context import ApplicationContext
from app.core.enums import CoordinateReferenceSystemEnum
from app.schemas.geometry.geometry_schema import CreateCircleSchema
from app.services.request_cache import RequestCacheService


class GeometryService:
    def __init__(
            self, context: ApplicationContext = Depends(ApplicationContext.get_context)
    ):
        self.context = context

    async def create_circle(
            self, data: CreateCircleSchema, request_cache_service: RequestCacheService
    ) -> str:
        """
        Создание окружности требуемого радиуса на основании долготы и широты
        """
        data_hash = request_cache_service.generate_request_hash(
            request_string=self._create_data_string(data)
        )
        async with self.context.database._session() as session:
            existent_geojson = await request_cache_service.find_data_by_hash(
                session, data_hash
            )
            if existent_geojson:
                return existent_geojson

            # Имитация тяжелой обработки
            await asyncio.sleep(6)

            point = func.ST_Point(data.coordinates.longitude, data.coordinates.latitude)
            circle = func.ST_Buffer(point, data.radius, quad_segs=8)

            geojson = await self.transform_to_geojson(session, circle)

            # Кэширование нового geojson'а
            await request_cache_service.create_request_hash(
                session, data_hash=data_hash, data=geojson
            )

        return geojson

    async def transform_to_geojson(
            self,
            session: AsyncSession,
            geometry: Geometry,
            srid: int = CoordinateReferenceSystemEnum.WGS_84.srid,
    ) -> Any:
        """
        Преобразование в geojson формат
        """
        result = await session.execute(func.ST_AsGeoJSON(geometry, srid))
        return result.scalar()

    def _create_data_string(self, data: CreateCircleSchema) -> str:
        """
        Формирование строки
        """
        return f"{data.coordinates.longitude}.{data.coordinates.latitude}.{data.radius}"
