from fastapi import (
    Depends,
    status,
)
from starlette.responses import JSONResponse

from app.core.context import ApplicationContext
from app.schemas.user.user_data import UserAuthorizationSchema
from app.services.security import SecurityService


class AuthService:
    def __init__(
        self,
        context: ApplicationContext = Depends(ApplicationContext.get_context),
        security_service: SecurityService = Depends(),
    ):
        self.context = context
        self.security_service = security_service

    def authorize(self, data: UserAuthorizationSchema) -> JSONResponse:
        """
        Затычка для получения токена авторизации
        """
        token = self.security_service.create_access_token(
            data={"username": data.username}
        )

        return self.create_response(
            access_token=token, description="Вы успешно авторизовались!"
        )

    @staticmethod
    def create_response(access_token: str, description: str) -> JSONResponse:
        response_with_cookie = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "description": description,
                "jwt_token": access_token,
            },
        )
        response_with_cookie.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="none",
            secure=True,
        )
        return response_with_cookie
