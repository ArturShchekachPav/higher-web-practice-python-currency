from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserDTO(BaseModel):
    """Тело запроса на создание пользователя."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)


class UpdateUserDTO(CreateUserDTO):
    pass


class UserDTO(BaseModel):
    """Тело ответа с данными пользователя без пароля."""

    id: int
    created_at: datetime
    updated_at: datetime
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
