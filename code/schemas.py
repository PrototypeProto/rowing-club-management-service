from pydantic import BaseModel
import uuid
from datetime import date, datetime
from sqlmodel import SQLModel

class User(BaseModel):
    uid: uuid.UUID
    username: str
    pwd: str
    user_description: str
    is_male: bool
    date_created: date
    time_modified: datetime

class UserCreateModel(BaseModel):
    username: str
    pwd: str
    user_description: str
    is_male: bool
    date_created: date
    time_modified: str


class UserUpdateModel(BaseModel):
    username: str
    pwd: str
    user_description: str
    is_male: bool
    time_modified: str
