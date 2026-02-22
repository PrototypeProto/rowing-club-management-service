from sqlmodel import SQLModel, Field, Column
from datetime import date, datetime, time
import uuid
import sqlalchemy.dialects.postgresql as postgres
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Time as Time
from enum import Enum

class SemesterEnum(str, Enum):
    '''
        NO practice during the summer, but placeholder in case situation changes
    '''
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"

class User(SQLModel, table=True):
    """
    How we access data from the database with an object that maps to corresponding parts,
        outline constraints and other behavior
    """

    __tablename__ = "User"

    uid: uuid.UUID = Field(
        sa_column=Column(
            postgres.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    username: str = Field(
        sa_column=Column(postgres.VARCHAR, nullable=False, unique=True)
    )
    email: str = Field(sa_column=Column(postgres.VARCHAR, unique=True, nullable=False))
    passwd_hash: str = Field(exclude=True)
    role: str = Field(foreign_key="MemberRole.role")
    is_verified: bool = Field(default=False)
    date_created: date = Field(sa_column=Column(postgres.DATE, default=date.today))
    time_modified: datetime = Field(
        sa_column=Column(postgres.TIMESTAMP, default=datetime.now)
    )

    def __repr__(self):
        return f"<User {self.username} + {self.uid}>"


class Product(SQLModel, table=True):
    """
    the ORM for products
    """

    __tablename__ = "Product"

    uid: uuid.UUID = Field(
        sa_column=Column(
            postgres.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    product_name: str
    product_description: str = Field(sa_column=Column(postgres.TEXT, default=""))
    revision_number: int
    date_introduced: date = Field(sa_column=Column(postgres.DATE, default=date.today))
    time_modified: datetime = Field(
        sa_column=Column(postgres.TIMESTAMP, default=datetime.now)
    )

    def __repr__(self):
        return f"<User {self.product_name} + {self.uid}>"


class MemberRole(SQLModel, table=True):
    """
    May deprecate ADMIN role in favor of president+VP role, TBD
    """

    __tablename__ = "MemberRole"

    role: str = Field(
        sa_column=Column(postgres.VARCHAR, primary_key=True, nullable=False)
    )
    # ADMIN = "admin"
    # COACH = "coach"
    # OFFICER = "officer"
    # MEMBER = "member"
    # INACTIVE = "inactive"


class Semester(SQLModel, table=True):
    """
    NO practice during the summer, but placeholder in case situation changes
    """

    __tablename__ = "Semester"

    semester: SemesterEnum = Field(
        sa_column=Column(postgres.VARCHAR, primary_key=True, nullable=False)
    )
    year: int = Field(primary_key=True, ge=1900, nullable=False)

    # Back reference
    absences: List["SemesterAbsence"] = Relationship(
        back_populates="semester_rel"
    )

    # SPRING = "spring"
    # SUMMER = "summer"
    # FALL = "fall"


class Coxwain(SQLModel, table=True):
    """
    Marks members that are coxwains
    """

    __tablename__ = "Coxwain"

    cox_id: uuid.UUID = Field(foreign_key="User.uid", primary_key=True)


class CoxwainEvaluation(SQLModel, table=True):
    """
    Anonymous feedback on a coxwain's abilities and suggestions from rowers
    """

    __tablename__ = "CoxwainEvaluation"

    evaluation_id: uuid.UUID = Field(
        sa_column=Column(
            postgres.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    cox_id: uuid.UUID = Field(foreign_key="User.uid", index=True)
    semester: SemesterEnum = Field(foreign_key="Semester.semester", index=True)
    year: int = Field(ge=1900, index=True)
    feedback: str = Field(sa_column=Column(postgres.TEXT, nullable=False))


class Rower(SQLModel, table=True):
    """
    A member that rows
    """

    __tablename__ = "Rower"

    rower_id: uuid.UUID = Field(foreign_key="User.uid", primary_key=True)


class RolePermissions(SQLModel, table=True):
    """
    Restricts certain APIs based on these permissions
    """

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
    """
    Tracks membership status on a per-semester basis
    """

    __tablename__ = "MemberEnrollmentHistory"

    member_id: uuid.UUID = Field(foreign_key="User.uid", primary_key=True)
    year: int = Field(ge=1900, primary_key=True)
    semester: SemesterEnum = Field(foreign_key="Semester.semester", primary_key=True)
    role: str = Field(foreign_key="MemberRole.role", default="inactive")
    dues_paid: bool = False

##############
'''

    WORKOUTS SECTION

'''
##############

class Workout(SQLModel, table=True):
    """ 
        A collection of similar workouts and the root parent
        Each day has its own set of workouts
        sequence_num refers to chronological ordering of the workouts done
    """

    __tablename__ = "Workout"

    workout_id: int = Field(
        sa_column=Column(
            primary_key=True, nullable=False
        )
    )

    date_occurred: date = Field(postgres.DATE, index=True)
    workout: str = Field(sa_column=Column(postgres.VARCHAR, nullable=False, index=True))
    sequence_num: int = Field(ge=1)
    
    desc: str = Field(
        sa_column=Column(
            postgres.TEXT,
            nullable=True,
        )
    )

class WorkoutType(str, Enum):
    '''
        Helper enum to validate input, workouts are the following 3 types
    '''
    DISTANCE = 'distance'
    TIME = 'time'
    MILERUN = 'mile_run'
    # WATER = 'water' # SHould be part of its own table, different measurements req

class WorkoutRoutine(SQLModel, table=True):
    '''
        Individual sub workout, maps to a parent workout
        workouts may vary by type, distance, timed, or a mile run
        with an optional requirment of min pacing, where NULL represents no cap, typically go all out or inapplicable such as in the mile run

        Used to not duplcate similar workouts
        A macro type?

        TODO: Figure out how to name/identify these table
        NOTE: Might have repeated values in the DB but negligent/can improve later
        NOTE: May move (workout_type, value, target_rate) to its own table and use it as a fk
        NOTE: too much abstraction may be miserable to read, will depend on how its like during API dev, esp. frontend
    '''
    __tablename__ = "WorkoutRoutine"

    routine_id: int = Field(primary_key=True)

    workout_id: int = Field(foreign_key="Workout.workout_id", index=True)
    sequence_num: int = Field(ge=1, index=True)

    workout_type: WorkoutType = Field(
        sa_column=Column(
            SAEnum(WorkoutType, name="workout_type_enum"),
            nullable=False,
            index=True
        )
    )
    value: int = Field(ge=1, index=True) # can represent meters OR seconds depending on `workout_type`
    target_rate: Optional[int] = Field(postgres.INTEGER, ge=1, default=None, nullable=True, index=True)

class MemberWorkoutPerformance(SQLModel, table=True):
    '''
        Members self report their score (sometimes reported by officers/coaches)
    '''
    __tablename__ = "MemberWorkoutPerformance"

    workout_performed_id: int = Field(foreign_key="WorkoutRoutine.routine_id", primary_key=True)
    member_id: uuid.UUID = Field(foreign_key="User.uid", primary_key=True)

    rate: Optional[int] = Field(default=None, index=True)
    wattage: Optional[int] = Field(default=None, index=True)
    time_to_completion: time = Field(
        sa_column=Column(
            postgres.TIME, nullable=False, index=True
        )
    )

class SemesterAbsence(SQLModel, table=True):
    '''
        Tracks each students's absences that semster, if not absent on that day then they were present
        Depends on a valid Semester entry

        TODO: tardiness is calculated by the practice date's start time(?)
    '''
    __tablename__ = "SemesterAbsence"

    __table_args__ = (
        ForeignKeyConstraint(
            ["Semester", "year"],
            ["Semester.semester", "Semester.year"],
            ondelete="CASCADE",
        ),
    )

    member_id: uuid.UUID = Field(foreign_key="User.uid", primary_key=True)
    semester: SemesterEnum = Field(primary_key=True)
    year: int = Field(ge=1900, primary_key=True)
    day: date = Field(primary_key=True)

    arrival_time: Optional[time] = None

    # Relationship to Semester
    semester_rel: Optional[Semester] = Relationship(
        back_populates="absences"
    )