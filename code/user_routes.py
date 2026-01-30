from typing import Optional, Union, Annotated, List
'''
    Optional[type(s)]
    Union() or (type | None)
    Annotated[type, "annotation textr"]
'''
from fastapi import FastAPI, Header, APIRouter, Depends
from fastapi import status
from fastapi.exceptions import HTTPException
# update models to edit
from .schemas import UserUpdateModel, UserCreateModel 
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from .models import User
from ..db.main import get_session


router_at_users = APIRouter()
user_service = UserService()



@router_at_users.post("/")
async def create_user(user_data: User, session: AsyncSession = Depends(get_session)) -> dict:
    new_user = await user_service.create_user(user_data, session)
    return new_user


@router_at_users.get("/all", response_model=List[User])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)
    return users

@router_at_users.get("/{user_uid}")
async def get_user(user_uid: int, session: AsyncSession = Depends(get_session)) -> dict:
    user = await user_service.get_user(user_uid, session)

    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")



@router_at_users.patch("/{user_uid}")
async def update_user(user_uid: str, user_update_data: UserUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
    updated_user = await user_service.update_user(user_uid, user_update_data, session)
        
    if updated_user:
        return updated_user

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


@router_at_users.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_uid:str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await user_service.delete_user(user_uid, session)

    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

