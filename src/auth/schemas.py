from pydantic import BaseModel, Field
import uuid
from datetime import date, datetime
from sqlmodel import SQLModel

'''
    What we use to enforce data input
'''


class User(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    passwd_hash: str = Field(exclude=True)
    role: str
    is_verified: bool = False
    date_created: date
    time_modified: datetime

class UserCreateModel(BaseModel):
    username: str = Field(max_length=12)
    email: str = Field(max_length=32)
    passwd: str = Field(min_length=6)

class UserUpdateModel(BaseModel):
    email: str
    passwd: str

class UserLoginModel(BaseModel):
    email: str
    passwd: str