from fastapi import APIRouter, status, HTTPException
from domain.auth.service import AuthService
from domain.auth.dto import Token, Login, Refresh
from domain.auth.exceptions import InvalidTokenError, CredentialsError
from core.deps import SessionDep


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=Token)
async def login(
    obj_in: Login,
    session: SessionDep
):
    service = AuthService(session)
    try:
        return await service.login(obj_in)
    except CredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )


@router.post('/refresh', response_model=Token)
async def refresh_tokens(
    obj_in: Refresh,
    session: SessionDep
):
    service = AuthService(session)
    try:
        return await service.refresh_tokens(obj_in)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )