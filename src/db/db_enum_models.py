from enum import Enum


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
    UNREGISTERED account on sign up, then once verified email
    WAIT_APPROVAL when verified but not approved by an officer on official joining of club
    ALUMNI is a former member of the club but no longer rows due to having graduated
    INACTIVE is currently a member of the club and is not currently participating in the current semester
    """

    ADMIN = "admin"
    COACH = "coach"
    OFFICER = "officer"
    MEMBER = "member"
    INACTIVE = "inactive"
    ALUMNI = "alumni"
    WAIT_APPROVAL = "wait_for_approval"
    UNREGISTERED = "unregistered"


class WorkoutTypeEnum(str, Enum):
    """
    Name workouts types
    """

    ERG = "erg"
    MILERUN = "mile_run"
    WATER = "water"


class WorkoutMeasurementTypeEnum(str, Enum):
    """
    Different ways to evalaute a workout
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

