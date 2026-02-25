from pydantic import BaseModel, Field, Union
from uuid import UUID
from datetime import date, datetime, time
from enum import Enum

# Prevent the addition of extra fields
class StrictModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }



class AttendanceType(str, Enum):
    '''
        NOTE: maybe remove the enums and make to normal data struct
        "Present" is omitted intentionally to reduce noise
    '''
    ABSENT = "absent"
    ABSENT_EXC = "excused_absence"
    TARDY = "tardy"
    TARDY_EXC = "excused_tardy"

class DateType(str, Enum):
    '''
        NOTE: maybe remove the enums and make to normal data struct
        The different kinds of activities that may occur in this club
        NOTE: Water/Land may be broken down to more specific workouts
            e.g. Steady-state, race-pace, etc.
    '''
    date_type: str
    description: str
    date_color: str = Field(min_length=6, max_length=6)

    # WATER = "On the water practice" 
    # LAND = "On the land practice" 

    # WEEKEND_PRACTICE = "Special weekend practice for upcoming matches" 
    # OYO = "On your own workout" 
    # SETUP = "Light practice / Load up gear on trailer" 
    # AWAY_SCRIMMAGE = "Away for scrimmage at another team's place" 
    # HOME_SCRIMMAGE = "Hosting scrimmage against another team" 
    # REGATTA = "Away for official regatta competition" 
    # VOLUNTEER = "Volunteering manpower at university event for club funding" 
    # FUNDRAISING = "Raising funds for the team" 

# class DateTypeColor(str, Enum):
#     '''
#         Used for the eventual frontend implementation, where on a calendar, a day is color coded for when there is a club activity
#     '''
#     WATER = "#1f77b4"
#     LAND = "#ff7f0e"

#     WEEKEND_PRACTICE = "#2ca02c"
#     OYO = "#d62728"
#     SETUP = "#9467bd"
#     AWAY_SCRIMMAGE = "#8c564b"
#     HOME_SCRIMMAGE = "#e377c2"
#     REGATTA = "#7f7f7f"
#     VOLUNTEER = "#bcbd22"
#     FUNDRAISING = "#17becf"


class Attendance(StrictModel):
    '''
        By default, omit the "present" type a
    '''
    uid: UUID
    date: date
    presence_status: AttendanceType

class ScheduledMeetings(StrictModel):
    '''
        Used to display information on active club dates
        NOTE: there isnt a date when more than 1 activity occurs
    '''
    date: date
    date_type: DateType
    time: str = Field(min_length=8, max_length=8) # "HR:MN {AM/PM}"
    ext_description: Union[str, None]

class ScheduledAttendance(StrictModel):
    '''
        Data here is subject to change as availability changes from week-to-week
        false = absent that day
        true = present that day
        NOTE: can use a bitmap first 7 bits are mon-sun
    '''
    uid: UUID
    mon: bool = False
    tue: bool = False
    wed: bool = False
    thu: bool = False
    fri: bool = False
    sat: bool = False
    sun: bool = False