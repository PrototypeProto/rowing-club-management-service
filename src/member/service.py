from src.db.models import *
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import *
from sqlmodel import select, desc, delete, update
from datetime import date, datetime
from uuid import UUID
from src.auth.service import UserService
from typing import List
from src.db.db_enum_models import MemberRoleEnum

user_service = UserService()


class MemberService:

    async def create_coxain(self, cox: CoxwainModel, session: AsyncSession) -> Coxwain:
        new_cox = Coxwain(**cox.model_dump())

        session.add(new_cox)
        await session.commit()
        return new_cox

    async def create_coxwain_evaluation(
        self, cox: CoxwainEvaluationModel, session: AsyncSession
    ) -> CoxwainModel:
        new_eval = CoxwainEvaluation(**cox.model_dump())

        session.add(new_eval)
        await session.commit()
        return new_eval

    async def get_one_coxwain_evaluation(
        self, cox_eval: SearchSpecificCoxwainEvaluationModel, session: AsyncSession
    ) -> CoxwainEvaluationModel:
        query = select(CoxwainEvaluation).where(
            CoxwainEvaluation.evaluation_id == cox_eval.evaluation_id
        )

        result = await session.exec(query)
        return result.first()

    async def remove_one_coxwain_evaluation(
        self, cox_eval: DeleteCoxwainEvaluationModel, session: AsyncSession
    ) -> bool:
        cox_evaluation = await self.get_one_coxwain_evaluation(cox_eval.evaluation_id, session)

        if cox_evaluation is None:
            return False

        print(cox_evaluation)

        await session.delete(cox_evaluation)
        await session.commit()
        return True

    async def get_all_coxwain_evaluations(
        self, cox: CoxwainModel, session: AsyncSession
    ):
        query = select(CoxwainEvaluation).where(Coxwain.cox_id == cox.cox_id)

        # for field_name, value in cox.dict(exclude_none=True).items():
        #     column = getattr(CoxwainEvaluation, field_name)
        #     query = query.where(column == value)

        result = await session.exec(query)
        return result.all()

    async def rower_exists(self, rower: RowerModel, session: AsyncSession) -> bool:
        query = select(Rower).where(Rower.rower_id == rower.rower_id)

        result = await session.exec(query)
        return result.first() is not None

    async def create_rower(self, rower: RowerModel, session: AsyncSession):
        if self.rower_exists(rower, session):
            return None

        new_rower = Rower(**rower.model_dump())

        session.add(new_rower)
        await session.commit()
        return new_rower

    async def get_role_permissions(self, role: MemberRoleEnum, session: AsyncSession) -> dict:
        query = select(RolePermissions).where(RolePermissions.role == role)

        result = await session.exec(query)
        return result.first()

    async def update_role_permissions(
        self, params: RolePermissionsUpdateModel, session: AsyncSession
    ) -> bool:
        role_permission = await self.get_role_permissions(params.role, session)

        if role_permission is None:
            return False

        # Get only the Columns which are marked to be bool-flipped
        toggle_fields = params.model_dump(exclude={"role"}, exclude_unset=True)

        # Create dict
        update_values = {
            field: ~getattr(RolePermissions, field)
            for field, value in toggle_fields.items()
            if value is True
        }

        statement = (
            update(RolePermissions)
            .where(RolePermissions.role == params.role)
            .values(**update_values)
        )

        result = await session.exec(statement)
        await session.commit()

        return result.rowcount > 0

    async def check_member_status(
        self, member: UserSearchModel, session: AsyncSession
    ):
        # query = select(MemberEnrollmentHistory)
        query = select(User.role).where(User.uid == member.uid)

        # for field_name, value in member.dict(exclude_none=True).items():
        #     column = getattr(MemberEnrollmentHistory, field_name)
        #     query = query.where(column == value)

        result = await session.exec(query)
        return result.first()

    # TODO: create a get semester ID method for this method and future methods
    # Update logic here for future to check if the enrollment history already has it populated
    async def enroll_member(
        self, add_member: CreateMemberEnrollmentHistoryModel, session: AsyncSession
    ) -> bool:
        user = await user_service.get_user_by_uid(add_member.member_id, session)
        if user is None:
            return False

        if await self.check_member_status(add_member, session) is not None:
            return False

        new_member_enrollment = MemberEnrollmentHistory(**add_member.model_dump())

        session.add(new_member_enrollment)
        await session.commit()
        return True

    async def raise_p(
        self, user_id: UUID, model: UserPrivilegeUpdateModel, session: AsyncSession
    ):
        statement = update(User).where(User.uid == user_id).values(model)
        result = await session.exec(statement)
        await session.commit()

        return result.rowcount > 0
