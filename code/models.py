from sqlmodel import SQLModel, Field, Column
from datetime import date, datetime
import uuid
import sqlalchemy.dialects.postgresql as postgres

class User(SQLModel, table=True):
    __tablename__ = "Users"
    
    uid: uuid.UUID = Field(
        sa_column = Column(
            postgres.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    pwd: str
    user_description: str
    is_male: bool
    date_created: date = Field (
        sa_column = Column(
            postgres.DATE, default=date.today
        )
    )
    time_modified: datetime = Field (
        sa_column = Column(
            postgres.TIMESTAMP, default=datetime.now
        )
    )

    def __repr__(self):
        return f"<User {self.uid}: user {self.username}>"


# 3:15