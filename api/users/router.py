from fastapi import APIRouter, status, HTTPException
from core.deps import SessionDep, UserDep, RequireUser
from domain.users.dto import CreateUserDTO, UpdateUserDTO, UserDTO
from domain.users.service import UserService
from domain.users.exceptions import UserNotFoundError, UserAlreadyExistsError


router = APIRouter(prefix='/users', tags=['users'])

@router.post(
    '/register',
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED
)
async def register(
    obj_in: CreateUserDTO,
    session: SessionDep
):
    service = UserService(session)
    try:
        return await service.create_user(obj_in)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )


@router.get('/{user_id}', response_model=UserDTO, dependencies=[RequireUser])
async def get_user_by_id(
    user_id: int,
    session: SessionDep
):
    service = UserService(session)
    try:
        return await service.get_user_by_id(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )


@router.get("/email/{email}", response_model=UserDTO, dependencies=[RequireUser])
async def get_user_by_email(
    email: str,
    session: SessionDep
):
    service = UserService(session)
    try:
        return await service.get_user_by_email(email)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )


@router.put('', response_model=UserDTO)
async def update_user(
    obj_in: UpdateUserDTO,
    session: SessionDep,
    current_user: UserDep
):
    service = UserService(session)
    try:
        return await service.update_user(obj_in, current_user)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )