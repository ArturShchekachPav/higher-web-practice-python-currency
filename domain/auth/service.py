from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.security import verify_password
from domain.auth.dto import Login, Refresh, Token, TokenPayload
from domain.auth.exceptions import CredentialsError, InvalidTokenError
from domain.users.exceptions import UserNotFoundError
from domain.users.service import UserService

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def decode_token(token: str, expected_type: str | None = None) -> TokenPayload:
    payload = jwt.decode(token, settings.secret, algorithms=[ALGORITHM])
    if expected_type is not None and payload.get("type") != expected_type:
        raise JWTError(f"Неверный тип токена: ожидался {expected_type}")
    return TokenPayload(
        user_id=payload["user_id"],
        email=payload["email"],
        exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
    )


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session)

    async def login(self, obj_in: Login) -> Token:
        """Аутентифицировать пользователя и создать токены.

        :param email: Адрес электронной почты пользователя
        :param password: Пароль в виде обычного текста
        :return: Объект токена с access и refresh токенами
        :raises CredentialsError: Если учетные данные недействительны
        """
        try:
            user = await self.user_service.get_user_by_email(obj_in.email)
        except UserNotFoundError as error:
            raise CredentialsError(
                f"Пользователь с email {obj_in.email} не найден!"
            ) from error
        if not verify_password(obj_in.password, user.hashed_password):
            raise CredentialsError(
                f"Пароль не подходит для пользователя с id {user.id}"
            )
        return Token(
            access_token=self._create_access_token(user.id, user.email),
            refresh_token=self._create_refresh_token(user.id, user.email),
        )

    async def refresh_tokens(self, obj_in: Refresh) -> Token:
        """Обновить access токен, используя refresh токен.

        :param refresh_token: Строка refresh токена
        :return: Новый объект токена с обновленными access и refresh токенами
        """
        try:
            payload = decode_token(
                obj_in.refresh_token, expected_type="refresh"
            )
        except JWTError as error:
            raise InvalidTokenError(
                "Неверный или истекший refresh токен"
            ) from error
        try:
            user = await self.user_service.get_user_by_id(payload.user_id)
        except UserNotFoundError as error:
            raise InvalidTokenError(
                f"Пользователь с id {payload.user_id} не найден!"
            ) from error
        return Token(
            access_token=self._create_access_token(user.id, user.email),
            refresh_token=self._create_refresh_token(user.id, user.email),
        )

    def _create_token(
        self,
        user_id: int,
        email: str,
        expires_delta: timedelta,
        token_type: str,
    ) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": now + expires_delta,
            "iat": now,
            "type": token_type,
        }
        return jwt.encode(payload, settings.secret, algorithm=ALGORITHM)

    def _create_access_token(self, user_id: int, email: str) -> str:
        return self._create_token(
            user_id,
            email,
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "access",
        )

    def _create_refresh_token(self, user_id: int, email: str) -> str:
        return self._create_token(
            user_id,
            email,
            timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "refresh",
        )
