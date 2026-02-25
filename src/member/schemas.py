from pydantic import BaseModel, Field
from pydantic import model_validator
from uuid import UUID
from datetime import date, datetime
from enum import Enum
from src.db.db_enum_models import MemberRoleEnum, SemesterEnum

class StrictModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }



class Coxwain(StrictModel):
    '''
        Marks members that are coxwains
    '''
    cox_id: UUID


class CoxwainEvaluationModel(StrictModel):
    evaluation_id: int 
    cox_id: UUID 
    semester_id: int 
    date_created: date
    feedback: str


class CreateCoxwainEvaluationModel(StrictModel):
    '''
        Submit 'anonymous' feedback on a coxwain's abilities and suggestions from rowers
        user submitted stored in logs not in DB
    '''
    cox_id: UUID
    semester: SemesterEnum
    feedback: str = Field(nullable=False)


class SearchCoxwainEvaluationModel(StrictModel):
    '''
        Anonymous feedback on a coxwain's abilities and suggestions from rowers
        Use `semester_id` to actually search
    '''
    cox_id: UUID
    semester: SemesterEnum
    year: int = Field(ge=1900)

class Rower(StrictModel):
    '''
        A member that rows
    '''
    rower_id: UUID

class RolePermissionsModel(StrictModel):
    '''
        Restricts certain APIs based on these permissions
    '''
    role: MemberRoleEnum
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
    role: MemberRoleEnum
    access_site: bool = False
    create_announcements: bool = False
    manage_dates: bool = False
    manage_members: bool = False
    manage_roles: bool = False
    view_funds: bool = False
    view_roster: bool = False

    @model_validator(mode="before")
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


class MemberEnrollmentHistoryModel(StrictModel):
    '''
        Tracks membership status on a per-semester basis
    '''
    member_id: UUID
    semester_id: int 
    role: MemberRoleEnum 
    dues_paid: bool

class CreateMemberEnrollmentHistoryModel(StrictModel):
    '''
        Tracks membership status on a per-semester basis
    '''
    member_id: UUID
    role: MemberRoleEnum
    year: int = Field(ge=1900, default=date.year)
    semester: SemesterEnum
    dues_paid: bool = False

class UserPrivilegeUpdateModel(StrictModel):
    role: str