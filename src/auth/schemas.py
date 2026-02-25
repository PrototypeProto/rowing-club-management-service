from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from src.db.db_enum_models import MemberRoleEnum

'''
    What we use to enforce data input
'''

class StrictModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }

class User(StrictModel):
    uid: UUID 
    username: str = Field(min_length=8, max_length=8)
    email: str = Field(max_length=32)
    passwd_hash: str = Field(exclude=True)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    role: MemberRoleEnum
    birthdate: date
    is_verified: bool
    join_date: date

class UserCreateModel(StrictModel):
    username: str = Field(max_length=12)
    email: str = Field(max_length=32)
    passwd: str = Field(min_length=6)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    birthdate: date
    role: MemberRoleEnum = MemberRoleEnum.UNREGISTERED

class UserChangePasswordModel(StrictModel):
    '''
    TODO: Perform safety checks on new passwd
    '''
    uid: UUID
    cur_passwd: str
    new_passwd: str

class UserLoginModel(StrictModel):
    username: str = Field(min_length=8, max_length=8)
    passwd: str = Field(min_length=6)

