from src.db.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateModel, UserUpdateModel, UserLoginModel
from sqlmodel import select, desc
from datetime import date, datetime
from .utils import generate_passwd_hash, verify_passwd
from uuid import UUID
from src.db.db_enum_models import MemberRoleEnum

"""
    Handles business logic (db access) for the {/users} route
    enforce proper data insertions 
"""


class UserService:
    """
    Service to access data related to user-data
    """

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Existence Validation - Log in / Sign up
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    async def username_exists(self, username: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_username(username, session)
        return user is not None

    async def get_user_by_username(self, username: str, session: AsyncSession) -> dict:
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first()

    async def email_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def get_user_by_email(self, email: str, session: AsyncSession) -> dict:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def uid_exists(self, uid: UUID, session: AsyncSession) -> bool:
        user = await self.get_user_by_uid(uid, session)
        return user is not None

    async def get_user_by_uid(self, uid: UUID, session: AsyncSession) -> dict:
        statement = select(User).where(User.uid == uid)
        result = await session.exec(statement)
        return result.first()
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Creation
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    async def create_user(
        self, user_data: UserCreateModel, session: AsyncSession
    ) -> User:
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)

        new_user.role = MemberRoleEnum.UNREGISTERED
        new_user.passwd_hash = generate_passwd_hash(user_data.passwd)
        new_user.join_date = date.today()
        new_user.is_verified = False

        session.add(new_user)
        await session.commit()
        return new_user

    # TODO: implement the login logic in the user_routes.py
    async def valid_user_login(
        self, user_login_details: UserLoginModel, session: AsyncSession
    ) -> bool:
        if not self.username_exists(user_login_details.username, session):
            return False

        statement = select(User.passwd_hash).where(
            User.username == user_login_details.username
        )
        result = await session.exec(statement)
        hashed_password = result.first()

        # Unnecessary?
        # if hashed_password is None:
        #     return false

        return verify_passwd(user_login_details.passwd, hashed_password)

    async def get_all_users(self, session: AsyncSession):
        statement = select(User).order_by(desc(User.join_date))

        result = await session.exec(statement)
        return result.all()

    # TODO: Create update user password method
    # async def update_user(self, user_uid:str, update_data:UserUpdateModel, session:AsyncSession):
    #     user_to_update = await self.get_user_by_email(user_uid, session)

    #     if user_to_update is not None:
    #         update_data_dict = update_data.model_dump()
    #         update_data_dict["time_modified"] = datetime.now()

    #         for k, v in update_data_dict.items():
    #             setattr(user_to_update, k, v)

    #         await session.commit()

    #         return user_to_update
    #     else:
    #         return None

    # async def delete_user(self, user_uid:str, session:AsyncSession) -> bool:
    #     user_to_delete = await self.get_user_by_email(user_uid, session)

    #     if user_to_delete is not None:
    #         await session.delete(user_to_delete)

    #         await session.commit()

    #         return True

    #     else:
    #         return False
