from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from auth.schemas import JWTSession
from auth.models import User, UserResponse
from auth.security import hash_password
from auth.dependencies import get_jwt_session
from .schemas import RegisterUser
from response import success

router = APIRouter(redirect_slashes=True)


@router.post("", response_model=UserResponse)
async def create_user(user_in: RegisterUser, _s: JWTSession = Depends(get_jwt_session)) -> Any:
    """Sign up."""
    user = await User.get_or_none(username=user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = await User.create(
        username=user_in.username, password_hash=hash_password(user_in.password)
    )
    return await UserResponse.from_tortoise_orm(user)


@router.get("", response_model=List[UserResponse])
async def get_users(_s: JWTSession = Depends(get_jwt_session)):
    return await UserResponse.from_queryset(User.all())


@router.get(
    "/{username}",
    response_model=UserResponse,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(username: str, _s: JWTSession = Depends(get_jwt_session)):
    return await UserResponse.from_queryset_single(User.get(username=username))


@router.delete("/{username}", response_model=Dict[str, bool], responses={404: {"model": HTTPNotFoundError}})
async def delete_user(username: str, _s: JWTSession = Depends(get_jwt_session)):
    deleted_count = await User.filter(username=username).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {username} not found")
    return success
