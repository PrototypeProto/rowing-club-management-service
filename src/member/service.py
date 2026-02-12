from src.db.models import *
from sqlmodel.ext.asyncio.session import AsyncSession
import src.member.schemas as sc
from sqlmodel import select, desc, delete, update
from datetime import date, datetime
from uuid import UUID
from src.auth.service import UserService

user_service = UserService()

class MemberService:

    async def create_coxain(self, cox: sc.Coxwain, session: AsyncSession) -> Coxwain:
        new_cox = Coxwain(**cox.model_dump())

        session.add(new_cox)
        await session.commit()
        
        return new_cox

    async def create_coxwain_evaluation(self, cox: sc.CoxwainEvaluation, session: AsyncSession) -> CoxwainEvaluationResponseModel:
        new_eval = CoxwainEvaluation(
            **cox.model_dump()
        )

        session.add(new_eval)
        await session.commit()

        return new_eval

    async def get_coxwain_evaluation(self, cox_eval: sc.CoxwainEvaluationSpecificModel, session: AsyncSession):
        query = select(CoxwainEvaluation).where(CoxwainEvaluation.evaluation_id == cox_eval.evaluation_id)

        result = await session.exec(query)
        return result.first()

    async def remove_coxwain_evaluation(self, cox_eval: sc.CoxwainEvaluationSpecificModel, session: AsyncSession) -> bool:
        cox_evaluation = await self.get_coxwain_evaluation(cox_eval, session)

        if (cox_evaluation is None):
            return False

        print(cox_evaluation)

        await session.delete(cox_evaluation)
        await session.commit()
        return True

    async def search_coxwain_evaluations(self, param: sc.CoxwainEvaluationSearchModel, session: AsyncSession):
        query = select(CoxwainEvaluation)
        
        for field_name, value in param.dict(exclude_none=True).items():
            column = getattr(CoxwainEvaluation, field_name)
            query = query.where(column == value)
        
        result = await session.exec(query)

        return result.all()

    async def rower_exists(self, rower: sc.Rower, session: AsyncSession) -> bool:
        query = select(Rower).where(Rower.rower_id == rower.rower_id)

        result = await session.exec(query)
        
        return result.first() is not None

    async def create_rower(self, rower: sc.Rower, session: AsyncSession):
        if self.rower_exists(rower, session):
            return None

        new_rower = Rower(
            **rower.model_dump()
        )

        session.add(new_rower)
        await session.commit()

        return new_rower

    async def get_role_permissions(self, role: str, session: AsyncSession) -> dict:
        query = select(RolePermissions).where(RolePermissions.role == role)

        result = await session.exec(query)
        return result.first()

    async def update_role_permissions(self, role: sc.RolePermissionsRequestUpdateModel, session: AsyncSession) -> bool:
        try:
            sc.MemberRole(role.role)
        except Exception:
            return False

        role_permission = await self.get_role_permissions(role.role, session)

        if role_permission is None:
            return False

        # Get only the Columns which are marked to be bool-flipped
        toggle_fields = role.model_dump(
            exclude={"role"},
            exclude_unset=True
        )

        # Create dict
        update_values = {
            field: ~getattr(RolePermissions, field) for field, value in toggle_fields.items() if value is True
        }

        statement = update(RolePermissions).where(RolePermissions.role == role.role).values(**update_values)

        result = await session.exec(statement)
        await session.commit()

        return result.rowcount > 0

    async def check_member_status(self, member: sc.MemberEnrollmentCreateModel, session: AsyncSession):
        query = select(MemberEnrollmentHistory)

        for field_name, value in member.dict(exclude_none=True).items():
            column = getattr(MemberEnrollmentHistory, field_name)
            query = query.where(column == value)
        
        result = await session.exec(query)

        return result.first()

    async def enroll_member(self, add_member: sc.MemberEnrollmentCreateModel, session: AsyncSession) -> bool:
        user = await user_service.get_user_by_uuid(add_member.member_id, session)
        if user is None:
            return False
        
        if await self.check_member_status(add_member, session) is not None:
            return False

        new_member_enrollment = MemberEnrollmentHistory(
            **add_member.model_dump()
        )

        session.add(new_member_enrollment)
        await session.commit()

        return True

    async def raise_p(self, user_id: UUID, model: sc.UserPrivilegeUpdateModel, session: AsyncSession):
        statement = update(User).where(User.uid == user_id).values(model)
        result = await session.exec(statement)
        await session.commit()

        return result.rowcount > 0