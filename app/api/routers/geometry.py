from fastapi import (
    Depends,
    Request,
)

from app.api.routers.utils import LoggingRouter
from app.core.decorations import auth_security_schema
from app.schemas.geometry.geometry_schema import CreateCircleSchema
from app.services.geometry import GeometryService
from app.services.request_cache import RequestCacheService

geometry_router = LoggingRouter(prefix="/api", tags=["Геометрия"])


@geometry_router.get(
    "/geometry/circle",
    description="Формирование PDF отчета по полной ипотеке",
)
async def create_circle_geometry(
    request: Request,
    data: CreateCircleSchema,
    token: str = Depends(auth_security_schema),
    geometry_service: GeometryService = Depends(),
    request_cache_service: RequestCacheService = Depends(),
) -> str:
    return await geometry_service.create_circle(data, request_cache_service)
