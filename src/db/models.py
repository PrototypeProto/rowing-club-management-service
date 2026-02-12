from sqlmodel import SQLModel, Field, Column
from datetime import date, datetime
import uuid
import sqlalchemy.dialects.postgresql as postgres

class User(SQLModel, table=True):
    '''
        How we access data from the database with an object that maps to corresponding parts, 
            outline constraints and other behavior
    '''

    __tablename__ = "User"
    
    uid: uuid.UUID = Field(
        sa_column = Column(
            postgres.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str = Field(
        sa_column = Column(
            postgres.VARCHAR,
            nullable=False,
            unique=True
        )
    )
    email: str = Field(
        sa_column=Column(
            postgres.VARCHAR,
            unique=True,
            nullable=False
        )
        
    )
    passwd_hash: str = Field(exclude=True)
    role: str = Field(
        foreign_key="MemberRole.role"
    )
    is_verified: bool = Field(default=False)
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
        return f"<User {self.username} + {self.uid}>"

class Product(SQLModel, table=True):
    '''
        the ORM for products
    '''
    __tablename__ = "Product"

    uid: uuid.UUID = Field(
        sa_column= Column(
            postgres.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    product_name: str
    product_description: str = Field(
        sa_column=Column(
            postgres.TEXT, default=""
        )
    )
    revision_number: int
    date_introduced: date = Field(
        sa_column=Column(
            postgres.DATE, default=date.today
        )
    )
    time_modified: datetime = Field(
        sa_column=Column(
            postgres.TIMESTAMP, default=datetime.now
        )
    )

    def __repr__(self):
        return f"<User {self.product_name} + {self.uid}>"

class MemberRole(SQLModel, table=True):
    '''
        May deprecate ADMIN role in favor of president+VP role, TBD
    '''
    __tablename__ = "MemberRole"

    role: str = Field(
        sa_column=Column(
            postgres.VARCHAR,
            primary_key=True,
            nullable=False
        )
    )
    # ADMIN = "admin"
    # COACH = "coach"
    # OFFICER = "officer"
    # MEMBER = "member"
    # INACTIVE = "inactive"

class Semester(SQLModel, table=True):
    '''
        NO practice during the summer, but placeholder in case situation changes
    '''
    __tablename__ = "Semester"

    semester: str = Field(
        sa_column=Column(
            postgres.VARCHAR,
            primary_key=True,
            nullable=False
        )
    )

    # SPRING = "spring"
    # SUMMER = "summer"
    # FALL = "fall"

class Coxwain(SQLModel, table=True):
    '''
        Marks members that are coxwains
    '''
    __tablename__ = "Coxwain"
    
    cox_id: uuid.UUID = Field(foreign_key="User.uid", primary_key=True)

class CoxwainEvaluation(SQLModel, table=True):
    '''
        Anonymous feedback on a coxwain's abilities and suggestions from rowers
    '''
    __tablename__ = "CoxwainEvaluation"
    
    evaluation_id: uuid.UUID = Field(
        sa_column = Column(
            postgres.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    cox_id: uuid.UUID = Field(foreign_key="User.uid", index=True)
    semester: str = Field(foreign_key="Semester.semester", index=True)
    year: int = Field(ge=1900, index=True)
    feedback: str = Field(
        sa_column=
        Column(
            postgres.TEXT,
            nullable=False
        )
    )

class Rower(SQLModel, table=True):
    '''
        A member that rows
    '''
    __tablename__ = "Rower"
    
    rower_id: uuid.UUID = Field(foreign_key="User.uid", primary_key=True)

class RolePermissions(SQLModel, table=True):
    '''
        Restricts certain APIs based on these permissions
    '''
    __tablename__ = "RolePermissions"
    
    role: str = Field(foreign_key="MemberRole.role", primary_key=True)
    access_site: bool
    create_announcements: bool
    manage_dates: bool
    manage_members: bool
    manage_roles: bool
    view_funds: bool
    view_roster: bool

class MemberEnrollmentHistory(SQLModel, table=True):
    '''
        Tracks membership status on a per-semester basis
    '''
    __tablename__ = "MemberEnrollmentHistory"
    
    member_id: uuid.UUID = Field(foreign_key="User.uid", primary_key=True)
    year: int = Field(ge=1900, primary_key=True)
    semester: str = Field(foreign_key="Semester.semester", primary_key=True)
    role: str = Field(foreign_key="MemberRole.role", default="inactive")
    dues_paid: bool = False


