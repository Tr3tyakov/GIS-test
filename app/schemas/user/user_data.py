from pydantic import (
    BaseModel,
    Field,
)


class UserAuthorizationSchema(BaseModel):
    username: str = Field(..., description="Имя пользователя")
    password: str = Field(..., description="Пароль пользователя")
