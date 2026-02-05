from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateModel, UserUpdateModel, UserLoginModel
from sqlmodel import select, desc
from datetime import date, datetime
from .utils import generate_passwd_hash, verify_passwd

'''
    Handles business logic (db access) for the {/users} route
    enforce proper data insertions 
'''

class UserService:

    async def get_user_by_email(self, email:str, session:AsyncSession) -> dict:
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user if user is not None else None

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def valid_user_login(self, user_login_details: UserLoginModel, session: AsyncSession) -> bool:
        if not self.user_exists(user_login_details.email, session):
            return False

        statement = select(User.passwd_hash).where(User.email == user_login_details.email)
        result = await session.exec(statement)
        hashed_password = result.first()

        if hashed_password is None:
            return false

        return verify_passwd(user_login_details.passwd, hashed_password)

    async def get_all_users(self, session:AsyncSession):
        statement = select(User).order_by(desc(User.date_created))

        result = await session.exec(statement)
        return result.all()

    async def create_user(self, user_data:UserCreateModel, session:AsyncSession) -> User:
        user_data_dict = user_data.model_dump()
        
        new_user = User(
            **user_data_dict
        )

        new_user.passwd_hash = generate_passwd_hash(user_data_dict['passwd'])

        session.add(new_user)

        await session.commit()

        return new_user

    async def update_user(self, user_uid:str, update_data:UserUpdateModel, session:AsyncSession):
        user_to_update = await self.get_user_by_email(user_uid, session)

        if user_to_update is not None:
            update_data_dict = update_data.model_dump()
            update_data_dict["time_modified"] = datetime.now()

            for k, v in update_data_dict.items():
                setattr(user_to_update, k, v)

            await session.commit()

            return user_to_update
        else:
            return None

    async def delete_user(self, user_uid:str, session:AsyncSession) -> bool:
        user_to_delete = await self.get_user_by_email(user_uid, session)

        if user_to_delete is not None:
            await session.delete(user_to_delete)

            await session.commit()

            return True
            
        else: 
            return False