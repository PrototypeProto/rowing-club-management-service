from typing import Optional, Union, Annotated, List
'''
    Optional[type(s)]
    Union() or (type | None)
    Annotated[type, "annotation textr"]
'''
from fastapi import FastAPI, Header, APIRouter, Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from .schemas import UserUpdateModel, UserCreateModel, User, UserLoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from src.db.main import get_session


'''
    A custom route to access users
    simple CRUD routes
    calls service() methods to perform business logic
'''

router_at_users = APIRouter()
user_service = UserService()



@router_at_users.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    email = user_data.email

    user_exists = await user_service.get_user_by_email(email, session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exists")

    new_user = await user_service.create_user(user_data, session)
    return new_user

@router_at_users.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    result = await user_service.valid_user_login(user_data, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid login attempt")

    

@router_at_users.get("/all", response_model=List[User])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)
    return users

@router_at_users.get("/{user_uid}", response_model=User)
async def get_user(user_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    user = await user_service.get_user(user_uid, session)

    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")



@router_at_users.patch("/{user_uid}", response_model=User)
async def update_user(user_uid: str, user_update_data: UserUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
    updated_user = await user_service.update_user(user_uid, user_update_data, session)
        
    if updated_user:
        return updated_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


@router_at_users.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_uid:str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await user_service.delete_user(user_uid, session)

    if not book_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

