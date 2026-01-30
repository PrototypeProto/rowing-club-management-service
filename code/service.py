from data_types import Users
from sqlmodel.ext.asyncio.session import AsyncSession
from schema import UserCreateModel, UserUpdateModel

class UserService:
    async def get_all_users(self, session:AsyncSession):
        pass

    async def get_user(self, user_uid:str, session:AsyncSession):
        pass

    async def create_user(self, user_data:UserCreateModel, session:AsyncSession):
        pass

    async def update_user(self, user_data:UserUpdateModel, session:AsyncSession):
        pass

    async def delete_user(self, user_uid:str, session:AsyncSession):
        pass