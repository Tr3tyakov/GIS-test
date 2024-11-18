from fastapi import (
    HTTPException,
    Request,
    status,
)
from fastapi.security import OAuth2PasswordBearer

from app.services.security import SecurityService


class AuthSecurity(OAuth2PasswordBearer):

    def __call__(self, request: Request):
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Отсутствует или недействителен токен",
            )

        security_service = SecurityService()
        user = security_service.validate_token(token=authorization.split(" ")[1])
        return user


auth_security_schema = AuthSecurity(tokenUrl="token")
