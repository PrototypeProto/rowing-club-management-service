from sqlmodel import SQLModel, Field, Column
from datetime import date, datetime, time, timedelta
from uuid import UUID
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Interval, Time as Time
from enum import Enum
import sqlalchemy.dialects.postgresql as postgres

"""##########################

    NOTE: START ENUM HELPERS 

##########################"""


class SemesterEnum(str, Enum):
    """
    NO practice during the summer, but placeholder in case situation changes
    """

    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"


class MemberRoleEnum(str, Enum):
    """
    May deprecate ADMIN role in favor of president+VP role, TBD
    """

    ADMIN = "admin"
    COACH = "coach"
    OFFICER = "officer"
    MEMBER = "member"
    INACTIVE = "inactive"


class WorkoutTypeEnum(str, Enum):
    """
    Helper enum to validate input, workouts are the following 3 types
    """

    ERG = "erg"
    MILERUN = "mile_run"
    WATER = "water"


class WorkoutMeasurementType(str, Enum):
    """
    Different means of measuring
    """

    DISTANCE = "distance"
    TIME = "time"
    WATTAGE = "wattage"


class BoatEnum(str, Enum):
    BUMBLEBEE = "bumble bee"
    GRIZZLE = "grizzle"
    WHEELER = "wheeler"
    JUDGE = "judge"
    VHP = "vhp"  # Vespoli?
    PHATB = "phat b"

    DZ = "d z"
    CLASS = "class"
    MJOLNIR = "mjolnir"
    SPACEU = "space u"


class BoatLineupTypeEnum(str, Enum):
    MEN = "men"
    WOMEN = "women"
    MIXED = "mixed"


"""##########################

    NOTE: END OF ENUM HELPERS

##########################"""

"""##########################

    NOTE: START USER DATA 

##########################"""


class User(SQLModel, table=True):
    """
    How we access data from the database with an object that maps to corresponding parts,
        outline constraints and other behavior

    username is typically nid, but not enforced as coaches may not have one
    """

    __tablename__ = "User"

    uid: UUID = Field(
        sa_column=Column(
            postgres.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )

    username: str = Field(
        sa_column=Column(postgres.VARCHAR, nullable=False, unique=True),
        min_length=8,
        max_length=8,
    )
    email: str = Field(sa_column=Column(postgres.VARCHAR, unique=True, nullable=False))
    passwd_hash: str = Field(postgres.VARCHAR, exclude=True)

    role: MemberRoleEnum = Field(
        sa_column=Column(
            SAEnum(MemberRoleEnum, name="member_role_enum", create_type=False),
            nullable=False,
            index=True,
        )
    )
    is_verified: bool = Field(default=False)
    join_date: date = Field(sa_column=Column(postgres.DATE, default=date.today))

    def __str__(self):
        return f"<User: {self.username} identified by id: {self.uid}>"


class Product(SQLModel, table=True):
    """
    the ORM for products
    NOTE: placeholder for now, to be removed
    """

    __tablename__ = "Product"

    uid: UUID = Field(
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


class Coxwain(SQLModel, table=True):
    """
    Marks members that are coxwains
    """

    __tablename__ = "Coxwain"

    cox_id: UUID = Field(foreign_key="User.uid", primary_key=True)


class CoxwainEvaluation(SQLModel, table=True):
    """
    Anonymous feedback on a coxwain's abilities and suggestions from rowers
    """

    __tablename__ = "CoxwainEvaluation"

    evaluation_id: int = Field(nullable=False, primary_key=True)

    cox_id: UUID = Field(foreign_key="User.uid", index=True)
    semester_id: int = Field(foreign_key="Semester.semester_id")
    date_created: date = Field(
        sa_column=Column(postgres.DATE, index=True, default=date.today)
    )

    feedback: str = Field(sa_column=Column(postgres.TEXT))


class Rower(SQLModel, table=True):
    """
    - Marks members that row
    - Uses the times a member has rowed to keep track of their expected pace contribution
    - `expected pace contribution` is total_pace_contribution / times_rowed, giving us the avg 500m pace of the user
    NOTE: this is flawed as strong rowers may be undervalued and weaker rowers being overvalued, but this is a simple/naive solution for now to keep it simple
    NOTE: Maybe use avg_wattage in the total_pace_contribution score later down the line and cumulatively add the scores factoring in the wattage to not have to keep track of change
    """

    __tablename__ = "Rower"

    rower_id: UUID = Field(foreign_key="User.uid", primary_key=True)

    times_rowed: int = Field(default=0, ge=0)
    avg_wattage: int = Field(default=0, ge=0)
    total_pace_contribution: int = Field(default=0, nullable=False, ge=0)
    personal_record_pace: Optional[timedelta] = Field(default=None)


class RolePermissions(SQLModel, table=True):
    """
    Restricts certain APIs based on these permissions
    """

    __tablename__ = "RolePermissions"

    role: MemberRoleEnum = Field(
        sa_column=Column(
            SAEnum(MemberRoleEnum, name="member_role_enum", create_type=False),
            nullable=False,
            primary_key=True,
        )
    )

    access_site: bool = False
    create_announcements: bool = False
    manage_dates: bool = False
    manage_members: bool = False
    manage_roles: bool = False
    view_funds: bool = False
    view_roster: bool = False


class MemberIssues(SQLModel, table=True):
    """
    Notes flaws/issues with a particular rower {im/material}
    rower should be aiming to fix these pointed out flaws
    """

    __tablename__ = "RowerIssues"

    issue_id: int = Field(primary_key=True, nullable=False)
    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)

    issue: str = Field(nullable=False)
    is_resolved: bool = False


class PerformanceExams(SQLModel, table=True):
    """
    Exams used to track performance over time
    """

    __tablename__ = "PerformanceExams"

    exam: str = Field(nullable=False, primary_key=True)

    workout_measurement_type: WorkoutMeasurementType = Field(
        sa_column=Column(
            SAEnum(
                WorkoutMeasurementType,
                name="workout_measurement_type_enum",
                create_type=False,
            )
        )
    )


class RecordedExams(SQLModel, table=True):
    """
    Exams used to track performance over time
    """

    __tablename__ = "RecordedExams"

    exam_id: int = Field(primary_key=True)

    exam: str = Field(foreign_key="PerformanceExams.exam", index=True)
    semester_id: int = Field(foreign_key="Semester.semester_id", index=True)
    date_occurred: date


class MemberExamPerformance(SQLModel, table=True):
    """
    NOTE: completion_time is the only non-optional due to milerun only measuring time
    NOTE: peak_wattage is for the watt ladder, where the rower reached that level b4 failing
    """

    __tablename__ = "MemberExamPerformance"

    exam_id: int = Field(foreign_key="RecordedExams.exam_id", primary_key=True)
    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)

    completion_time: timedelta
    avg_pace: Optional[timedelta]
    avg_rate: Optional[int]
    avg_wattage: Optional[int]
    peak_wattage: Optional[int]


class RowerPerformanceOverTime(SQLModel, table=True):
    """
    tracks PR over time
    """
    __tablename__ = "RowerPerformanceOverTime"

    exam: str = Field(foreign_key="PerformanceExams.exam", primary_key=True)
    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)
    date_occurred: date = Field(primary_key=True)

    value_int: Optional[int] = Field(default=None)
    value_time: Optional[timedelta] = Field(default=None)

# TODO: PR TABLES FOR DIFFERENT EXAMS {Mile runs, 5k, 2k, watt pyramid}

"""##########################

    NOTE: END USER DATA 

##########################"""

"""##########################

    NOTE: START WORKOUT DATA 

##########################"""


class Workout(SQLModel, table=True):
    """
    - A collection of similar workouts and the root parent
    - Each day has its own set of workouts
    - sequence_num refers to chronological ordering of different sets of workouts done on this day
    - e.g. `5x500m`

    + order by date, then by sequence_num
    """

    __tablename__ = "Workout"

    workout_id: int = Field(sa_column=Column(primary_key=True, nullable=False))

    date_occurred: date = Field(postgres.DATE, index=True)
    workout: str = Field(sa_column=Column(postgres.VARCHAR, nullable=False, index=True))
    workout_type: WorkoutTypeEnum = Field(
        sa_column=Column(
            SAEnum(WorkoutTypeEnum, name="workout_type_enum"),
            nullable=False,
            index=True,
        )
    )

    sequence_num: int = Field(ge=1)
    desc: str = Field(
        sa_column=Column(
            postgres.TEXT,
            nullable=True,
        )
    )


class WorkoutRoutine(SQLModel, table=True):
    """
    - NOTE: FOR LAND-BASED ACTIVITIES
    - Individual sub workout, maps to a parent workout
    - workouts may vary by distance, time, or a mile run
    - `target_rate` is an optional requirment, where NULL represents no cap,
        typically go all out or inapplicable such as in the mile run
    - `target_value` is either a distance (m), a time interval (min, sec) or wattage target

    NOTE: Might have repeated values in the DB but may be negligent/can improve later
    NOTE: May move (distance_or_duration, target_rate) to its own table and use it as a fk
    NOTE: too much abstraction may be miserable to read, will depend on how its like during API dev, esp. frontend
    """

    __tablename__ = "WorkoutRoutine"

    routine_id: int = Field(primary_key=True)

    workout_id: int = Field(foreign_key="Workout.workout_id", index=True)
    sequence_num: int = Field(ge=1, index=True)
    target_measurement_type: WorkoutMeasurementType = Field(
        sa_column=Column(
            SAEnum(
                WorkoutMeasurementType,
                name="workout_measurement_type",
                create_type=False,
            ),
            nullable=False,
            index=True,
        )
    )

    target_value: int = Field(
        ge=1, index=True
    )  # can represent meters OR seconds depending on `workout_type`
    target_rate: Optional[int] = Field(
        postgres.INTEGER, ge=1, default=None, nullable=True, index=True
    )
    # NOTE: FUTURE, add `TARGET_PACE`


class MemberWorkoutPerformance(SQLModel, table=True):
    """
    Members self report their score (sometimes reported by officers/coaches)
    avg_rate remains indexed for now NOTE: Subject to change
    NOTE: this is the best i could do for now since its not always where we measure all but sometimes we do
    """

    __tablename__ = "MemberWorkoutPerformance"

    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)
    workout_performed_id: int = Field(
        foreign_key="WorkoutRoutine.routine_id", primary_key=True
    )

    total_time: Optional[timedelta] = Field(
        sa_column=Column(Interval, default=None, nullable=True)
    )
    avg_pace: Optional[timedelta] = Field(
        sa_column=Column(Interval, default=None, nullable=True, index=True)
    )
    avg_rate: Optional[int] = Field(default=None, nullable=True)
    avg_wattage: Optional[int] = Field(default=None, nullable=True)


class BoatWorkoutRoutine(SQLModel, table=True):
    """
    NOTE: FOR WATER-BASED ACTIVITIES
    NOTE: Differs from the land-based due to boats having independent goals (Varsity vs Novice, men vs women)
    - Individual boat workout, maps to a parent workout
    - workouts may vary by distance or time
    - `target_rate` NULL represents no cap, full steam ahead
    - `target_rate` may also represent (min or max) rate? Sometimes it is variable rate

    NOTE: Might have repeated values in the DB but negligent/can improve later
    NOTE: May move (distance_or_duration, target_rate) to its own table and use it as a fk
    NOTE: too much abstraction may be miserable to read, will depend on how its like during API dev, esp. frontend
    NOTE: Unsure if `target_value` should be indexed or not

    """

    __tablename__ = "BoatWorkoutRoutine"

    boat_routine_id: int = Field(primary_key=True)

    workout_id: int = Field(foreign_key="Workout.workout_id", index=True)
    sequence_num: int = Field(ge=1, index=True)
    boat: BoatEnum = Field(
        sa_column=Column(
            SAEnum(BoatEnum, name="boat_name_enum", create_type=False),
            nullable=False,
            index=True,
        )
    )
    target_measurement_type: WorkoutMeasurementType = Field(
        sa_column=Column(
            SAEnum(
                WorkoutMeasurementType,
                name="workout_measurement_type_enum",
                create_type=False,
            ),
            nullable=False,
            index=True,
        )
    )

    target_value: int = Field(
        ge=1, index=False
    )  # can represent meters OR seconds depending on `workout_type`
    target_rate: Optional[int] = Field(
        postgres.INTEGER, ge=1, default=None, nullable=True, index=True
    )

    total_time: Optional[timedelta] = Field(
        sa_column=Column(Interval, default=None, nullable=True)
    )
    min_pace: Optional[timedelta] = Field(
        sa_column=Column(Interval, default=None, nullable=True)
    )
    max_pace: Optional[timedelta] = Field(
        sa_column=Column(Interval, default=None, nullable=True)
    )
    avg_pace: Optional[timedelta] = Field(
        sa_column=Column(Interval, default=None, nullable=True)
    )
    avg_rate: Optional[int] = Field(default=None, nullable=True)
    # NOTE: FUTURE, add `TARGET_PACE`


class BoatRoutineIdentifier(SQLModel, table=True):
    """
    Tracks the rowers and coxwain on a boat for a workout
    NOTE: this is probably messy and should have followed the style for land-based workout
    NOTE: probably tying it to the workout itself rather than subroutines because members dont often swap out from their boat
    NOTE: anticipated pace will estimate the boats pace using the combined avg of the rowers anticipated contribution pace
    """

    __tablename__ = "BoatRoutineIdentifier"

    boat_routine_id: int = Field(primary_key=True)

    workout_id: int = Field(foreign_key="Workout.workout_id", index=True)
    boat: BoatEnum = Field(
        sa_column=Column(
            SAEnum(BoatEnum, name="boat_name_enum", create_type=False), index=True
        )
    )
    coxwain_id: UUID = Field(foreign_key="Coxwain.cox_id", index=True)

    anticipated_pace: timedelta = Field(sa_column=Column(Interval, nullable=False))


class RowerOnBoat(SQLModel, table=True):
    """
    Track who was on a specific boat during the workout
    """

    __tablename__ = "RowerOnBoat"

    boat_routine_id: int = Field(
        foreign_key="BoatRoutineIdentifier.boat_routine_id", primary_key=True
    )
    rower_id: UUID = Field(foreign_key="Rower.rower_id", primary_key=True)

    seat_num: int = Field(ge=1, le=8)


class BoatFeedback(SQLModel, table=True):
    """
    Constructive criticism on the overall effort and feeling on the boat during the workout
    """

    __tablename__ = "BoatFeedback"

    boat_routine_id: int = Field(
        foreign_key="BoatWorkoutRoutine.boat_routine_id", primary_key=True
    )
    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)

    evaluation: str = Field(nullable=False)


"""##########################

    NOTE: END WORKOUT DATA 

##########################"""

"""##########################

    NOTE: START CALENDAR DATA 

##########################"""


class Semester(SQLModel, table=True):
    """
    NO practice during the summer, but placeholder in case situation changes
    """

    __tablename__ = "Semester"

    semester_id: int = Field(primary_key=True)

    year: int = Field(ge=1900, nullable=False, index=True)
    semester: SemesterEnum = Field(
        sa_column=Column(
            SAEnum(SemesterEnum, name="semester_enum", create_type=False),
            nullable=False,
            index=True,
        )
    )

    start_date: date = Field(postgres.DATE, index=True)
    end_date: date = Field(postgres.DATE, index=True)


class SemesterAbsence(SQLModel, table=True):
    """
    Tracks each students's absences that semster, if not absent on that day then they were present
    Depends on a valid Semester entry
    """

    __tablename__ = "SemesterAbsence"

    __table_args__ = (
        ForeignKeyConstraint(
            ["Semester", "year"],
            ["Semester.semester", "Semester.year"],
            ondelete="CASCADE",
        ),
    )

    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)
    date_occurred: date = Field(primary_key=True)

    semester_id: int = Field(foreign_key="Semester.semester_id", index=True)

    arrival_time: Optional[time] = None


class MemberEnrollmentHistory(SQLModel, table=True):
    """
    Tracks membership status on a per-semester basis
    """

    __tablename__ = "MemberEnrollmentHistory"

    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)
    semester_id: int = Field(foreign_key="Semester.semester_id", primary_key=True)

    role: MemberRoleEnum = Field(
        sa_column=Column(
            SAEnum(MemberRoleEnum, name="member_role_enum", create_type=False),
            nullable=False,
            default=MemberRoleEnum.INACTIVE,
        )
    )
    dues_paid: bool = False


class Availability(SQLModel, table=True):
    """
    - An evolving availability sheet for the week
    - Depends on `ScheduledAbsence` for atypical absences
    - should be deleted at the end of the semester and repopulated with active members (annoying)
    """

    __tablename__ = "Availability"

    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)

    present_monday: bool = Field(default=False, index=True)
    present_tuesday: bool = Field(default=False, index=True)
    present_wednesday: bool = Field(default=False, index=True)
    present_thursday: bool = Field(default=False, index=True)
    present_friday: bool = Field(default=False, index=True)
    present_saturday: bool = Field(default=False, index=True)
    present_sunday: bool = Field(default=False, index=True)


class ScheduledAbsence(SQLModel, table=True):
    """
    - Used to update `Availability` when planning an absence on a day where the user is normally present
    - Use some trigger to check all dates within a range (mon-sun of that week) and update availability
    - Delete on start of next week, so monday at 12:00 AM, midnight

    NOTE: Will ignore below for now, and assume a logical flip instead, so assume True
    NOTE: maybe use an override bitmask (7bits) to denote an explicit absence and set to 0 when no planned absences
        That way we don't need to keep track whether or not they were originally planning to come (inconsistent scheduling)
    """

    __tablename__ = "ScheduledAbsence"

    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)
    absence_date: date = Field(primary_key=True)


class VolunteeringDate(SQLModel, table=True):
    """
    Stores significant dates for when club has to do university-mandated volunteering
    """

    __tablename__ = "VolunteeringDate"

    volunteer_date: date = Field(primary_key=True)

    location: str
    min_heads_required: int = Field(ge=1, nullable=False)
    start_time: time = Field(sa_column=Column(postgres.TIME, nullable=False))
    end_time: Optional[time] = Field(sa_column=Column(postgres.TIME, nullable=True))


class RegisteredVolunteers(SQLModel, table=True):
    """
    Members who plan to volunteer
    volunteered becomes true once the supervisor approves attendance, otherwise SHAA~AME
    """

    __tablename__ = "RegisteredVolunteers"

    volunteer_date: date = Field(
        foreign_key="VolunteeringDate.volunteer_date", primary_key=True
    )
    member_id: UUID = Field(foreign_key="User.uid", primary_key=True)

    volunteered: bool = Field(default=False)


"""##########################

    NOTE: END CALENDAR DATA 

##########################"""

"""##########################

    NOTE: START BOAT DATA 

##########################"""


class BoatInfo(SQLModel, table=True):
    """
    Contains general data on a boat
    """

    __tablename__ = "BoatInfo"

    name: BoatEnum = Field(
        sa_column=Column(
            SAEnum(BoatEnum, name="boat_name_enum", create_type=False), primary_key=True
        )
    )

    weight_class: float
    seat_count: int = Field(ge=1, le=8)


class BoatIssues(SQLModel, table=True):
    """
    known existing and previous issues
    """

    __tablename__ = "BoatIssues"

    issue_id: int = Field(primary_key=True)

    name: BoatEnum = Field(
        sa_column=Column(
            SAEnum(BoatEnum, name="boat_name_enum", create_type=False), index=True
        )
    )
    remains_problematic: bool = Field(default=True, index=True)

    issue_description: str = Field(sa_column=Column(postgres.VARCHAR, nullable=True))


"""##########################

    NOTE: END BOAT DATA 

##########################"""


"""##########################

    NOTE: START GOLD & BLACK

##########################"""


"""##########################

    NOTE: END GOLD & BLACK

##########################"""
