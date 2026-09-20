

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_async_session
from domain.auth.service import decode_token
from domain.users.exceptions import UserNotFoundError
from domain.users.models import User
from domain.users.service import UserService


http_bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(credentials.credentials, expected_type="access")
    except JWTError:
        raise credentials_exception
    try:
        return await UserService(session).get_user_by_id(payload.user_id)
    except UserNotFoundError:
        raise credentials_exception