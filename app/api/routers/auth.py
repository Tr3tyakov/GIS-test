from fastapi import (
    Depends,
    Request,
)
from starlette.responses import JSONResponse

from app.api.routers.utils import LoggingRouter
from app.schemas.user.user_data import UserAuthorizationSchema
from app.services.auth import AuthService

auth_router = LoggingRouter(prefix="/api", tags=["Авторизация"])


@auth_router.get(
    "/authorize",
    description="Имитация авторизации пользователя для получения токена",
)
async def authorize(
    request: Request,
    data: UserAuthorizationSchema,
    auth_service: AuthService = Depends(),
) -> JSONResponse:
    return auth_service.authorize(data)
