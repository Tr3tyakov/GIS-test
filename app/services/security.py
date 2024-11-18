from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import (
    Any,
    Dict,
)

import jwt
from fastapi import (
    HTTPException,
    status,
)

from app.config import settings


class SecurityService:
    SECRET_KEY = settings.TOKEN.secret_key
    ALGORITHM = settings.TOKEN.algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.TOKEN.expire_minutes

    def validate_token(self, token: str) -> Dict[str, Any]:
        """Проверка валидности токена"""
        try:
            user_data = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Срок действия токена истек",
            )
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user_data

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Создание токена"""
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_jwt
