from pydantic import BaseModel, Field
from pydantic import model_validator
import uuid
from datetime import date, datetime
from enum import Enum

class StrictModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }

class MemberRole(str, Enum):
    '''
        May deprecate ADMIN role in favor of president+VP role, TBD
    '''
    ADMIN = "admin"
    COACH = "coach"
    OFFICER = "officer"
    MEMBER = "member"
    INACTIVE = "inactive"

class Semester(str, Enum):
    '''
        NO practice during the summer, but placeholder in case situation changes
    '''
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"



class Coxwain(StrictModel):
    '''
        Marks members that are coxwains
    '''
    cox_id: uuid.UUID

class CoxwainEvaluation(StrictModel):
    '''
        Anonymous feedback on a coxwain's abilities and suggestions from rowers
    '''
    cox_id: uuid.UUID
    semester: str
    year: int = Field(ge=1900)
    feedback: str

class CoxwainEvaluationResponseModel(StrictModel):
    evaluation_id: uuid.UUID
    cox_id: uuid.UUID
    semester: Semester
    year: int
    feedback: str

class CoxwainEvaluationSpecificModel(StrictModel):
    evaluation_id: uuid.UUID

class CoxwainEvaluationSearchModel(StrictModel):
    '''
        Anonymous feedback on a coxwain's abilities and suggestions from rowers
    '''
    cox_id: uuid.UUID
    semester: str
    year: int = Field(ge=1900)

class Rower(StrictModel):
    '''
        A member that rows
    '''
    rower_id: uuid.UUID

class RolePermissions(StrictModel):
    '''
        Restricts certain APIs based on these permissions
    '''
    role: MemberRole
    access_site: bool
    create_announcements: bool
    manage_dates: bool
    manage_members: bool
    manage_roles: bool
    view_funds: bool
    view_roster: bool

class RolePermissionsUpdateModel(StrictModel):
    '''
        Flips bool value in database where bool is true
    '''
    role: MemberRole
    access_site: bool = False
    create_announcements: bool = False
    manage_dates: bool = False
    manage_members: bool = False
    manage_roles: bool = False
    view_funds: bool = False
    view_roster: bool = False

    @model_validator(mode="after")
    def require_one(self):
        permissions = [
            self.access_site,
            self.create_announcements,
            self.manage_dates,
            self.manage_members,
            self.manage_roles,
            self.view_funds,
            self.view_roster,
        ]

        if not any(permissions):
            raise ValueError("At least one permission must be set to True")

        return self

class MemberEnrollment(StrictModel):
    '''
        Tracks membership status on a per-semester basis
    '''
    member_id: uuid.UUID
    year: int = Field(ge=1900)
    semester: str
    role: str 
    dues_paid: bool 

class MemberEnrollmentCreateModel(StrictModel):
    '''
        Tracks membership status on a per-semester basis
    '''
    member_id: uuid.UUID
    year: int = Field(ge=1900)
    semester: str

class UserPrivilegeUpdateModel(StrictModel):
    role: str