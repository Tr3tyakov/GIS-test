from app.api.routers.utils import LoggingRouter
from fastapi import Request, Depends

from app.core.context import ApplicationContext
from app.schemas.geometry.geometry_schema import CoordinateSchema, CreateCircleSchema
from app.services.geometry import GeometryService

geometry_router = LoggingRouter(prefix="/api", tags=["Геометрия"])


@geometry_router.get(
    "/report/full_mortgages/projects/{object_id}/mortgage/{mortgage_id}/bank/{bank_id}",
    description="Формирование PDF отчета по полной ипотеке",
)
async def create_circle_geometry(
        request: Request,
        context: ApplicationContext = Depends(ApplicationContext.get_context),
        service: GeometryService = Depends(),
        user_data: CreateCircleSchema
) -> str:
    return await service.create_circle(user_data)
