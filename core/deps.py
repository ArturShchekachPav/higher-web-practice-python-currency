from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from core.user import get_current_user
from domain.users.models import User

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
RequireUser = Depends(get_current_user)
UserDep = Annotated[User, RequireUser]
