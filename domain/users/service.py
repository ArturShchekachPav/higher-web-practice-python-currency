from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from domain.users.dto import CreateUserDTO, UpdateUserDTO
from domain.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.users.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, user_email: str) -> User:
        """Получить пользователя по адресу электронной почты.

        :param user_email: Адрес электронной почты пользователя
        :return: Объект модели пользователя
        :raises UserNotFoundError: Если пользователь с указанным email не существует
        """
        result = await self.session.execute(
            select(User).where(User.email == user_email)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError(
                f"Пользователь с email {user_email} не найден!"
            )
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        """Получить пользователя по ID.

        :param user_id: Идентификатор пользователя
        :return: Объект модели пользователя
        :raises UserNotFoundError: Если пользователь с указанным ID не существует
        """
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError(f"Пользователь с id {user_id} не найден!")
        return user

    async def create_user(self, obj_in: CreateUserDTO) -> User:
        """Создать нового пользователя.

        :param obj_in: Объект передачи данных для создания пользователя
        :return: Созданный объект модели пользователя
        :raises UserAlreadyExistsError: Если пользователь с указанным email уже существует
        """
        await self._check_user_email_duplicate(obj_in.email)
        new_user = User(
            email=obj_in.email,
            hashed_password=hash_password(obj_in.password),
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def update_user(self, obj_in: UpdateUserDTO, user: User) -> User:
        """Обновить существующего пользователя.

        :param obj_in: Объект передачи данных пользователя с паролем
        :return: Обновленный объект модели пользователя
        """
        if obj_in.email != user.email:
            await self._check_user_email_duplicate(obj_in.email)
        user.email = obj_in.email
        user.hashed_password = hash_password(obj_in.password)
        await self.session.flush()
        return user

    async def _check_user_email_duplicate(self, user_email: str):
        result = await self.session.execute(
            select(User).where(User.email == user_email)
        )
        user = result.scalar_one_or_none()
        if user is not None:
            raise UserAlreadyExistsError(
                f"Пользователь с email {user_email} уже существует!"
            )
