from typing import Optional, Union, Annotated, List
'''
    Optional[type(s)]
    Union() or (type | None)
    Annotated[type, "annotation textr"]
'''
from fastapi import FastAPI, Header, APIRouter, Depends
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.auth.schemas import User
from .schemas import *
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService
from src.db.main import get_session
from datetime import datetime, timedelta
from src.auth.dependencies import RefreshTokenBearer, access_token_bearer, get_current_user_email, get_current_user_uuid
from src.auth.dependencies_data import admin_rolechecker, coach_rolechecker, officer_rolechecker, member_rolechecker, public_rolechecker
from .service import MemberService
from uuid import UUID

REFRESH_TOKEN_EXPIRY_DAYS = 2


'''
    A custom route to access users
    simple CRUD routes
    calls service() methods to perform business logic
'''

member_router = APIRouter(dependencies=[access_token_bearer])
user_service = UserService()
member_service = MemberService()
SessionDependency = Annotated[AsyncSession, Depends(get_session)]


@member_router.post("/add_coxain", response_model=Coxwain, dependencies=[officer_rolechecker], status_code=status.HTTP_201_CREATED)
async def add_coxain(cox: Coxwain, session: SessionDependency):
    user_exists = await user_service.get_user_by_uuid(cox.cox_id, session)
    
    if user_exists is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Coxain is already a coxain")

    new_user = await member_service.create_coxain(cox, session)
    return new_user

@member_router.post("/submit_coxwain_evaluation", response_model=CoxwainEvaluationResponseModel, dependencies=[public_rolechecker])
async def evaluate_coxwain( cox_eval: CoxwainEvaluation, session: SessionDependency) -> dict:
    # TODO: log who sent feedback
    coxwain_eval = await member_service.create_coxwain_evaluation(cox_eval, session)

    if coxwain_eval is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user provided / Failed to submit evaluation")

    return coxwain_eval

@member_router.put("/raise_privilege", status_code=status.HTTP_202_ACCEPTED)
async def raise_privilege(session: SessionDependency, token: dict = access_token_bearer):
    details = token["user"]["uid"]

    result = await member_service.raise_p(details, {"role":"admin"}, session)
    if result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="failed..."
        )

# TODO: fix returning OK when not deleting the eval
@member_router.delete("/remove_coxwain_evaluation", dependencies=[officer_rolechecker], status_code=status.HTTP_204_NO_CONTENT)
async def del_coxwain_evaluation(cox_eval: CoxwainEvaluationSpecificModel, session: SessionDependency):
    if not await member_service.remove_coxwain_evaluation(cox_eval, session):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unable to remove selected coxwain evaluation"
        )

@member_router.put("/get_coxwain_evaluations", response_model=list[CoxwainEvaluation])
async def get_cox_evals(session: SessionDependency, eval_search_params: CoxwainEvaluationSearchModel):
    result = await member_service.search_coxwain_evaluations(eval_search_params, session)
    return result

# @member_router.put("/raise_privilege", status_code=status.HTTP_202_ACCEPTED)

# @member_router.put("/raise_privilege", status_code=status.HTTP_202_ACCEPTED)

# @member_router.put("/raise_privilege", status_code=status.HTTP_202_ACCEPTED)

# @member_router.put("/raise_privilege", status_code=status.HTTP_202_ACCEPTED)

# @member_router.put("/raise_privilege", status_code=status.HTTP_202_ACCEPTED)

# @member_router.put("/raise_privilege", status_code=status.HTTP_202_ACCEPTED)




# @member_router.post("/login", status_code=status.HTTP_200_OK)
# async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
#     email = login_data.email
#     passwd = login_data.passwd

#     user = await user_service.get_user_by_email(email, session)

#     if user is not None:
#         passwd_valid = verify_passwd(passwd, user.passwd_hash)

#         if passwd_valid:
#             access_token = create_access_token(
#                 user_data={
#                     "email": user.email,
#                     "uid": str(user.uid),
#                     "role": user.role,
#                 },
#             )

#             refresh_token = create_access_token(
#                 user_data={
#                     "email": user.email,
#                     "uid": str(user.uid),
#                 },
#                 refresh=True,
#                 expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
#             )

#             return JSONResponse(
#                 content={
#                     "message": "login successful",
#                     "access_token": access_token,
#                     "refresh_token": refresh_token,
#                     "user":{
#                         "email": user.email,
#                         "uid": str(user.uid)
#                     },
#                 }
#             )

#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email and/or password")

# @member_router.get("/all", response_model=List[User])
# async def get_all_users(session: AsyncSession = Depends(get_session)):
#     users = await user_service.get_all_users(session)
#     return users

# @member_router.get("/refresh_token")
# async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
#     expiry_timestamp = token_details['exp']

#     if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
#         new_access_token = create_access_token(
#             user_data=token_details['user']
#         )

#         return JSONResponse(content={
#             "access_token": new_access_token
#         })

#     raise HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid/Expired token"
#     )

# @member_router.get('/me', dependencies=[role_checker])
# async def get_current_user(user = Depends(get_current_user_email)):
#     return user

# @member_router.get("/logout", dependencies=[role_checker])
# async def revoke_token(token_details: dict = Depends(AccessTokenBearer)):
#     jti = token_details['jti']

#     await add_jti_to_blocklist(jti)

#     return JSONResponse(
#         content={
#             "message": "Logged out successfully"
#         },
#         status_code=status.HTTP_200_OK
#     )

# @member_router.get("/{user_uid}", response_model=User)
# async def get_user(user_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
#     user = await user_service.get_user(user_uid, session)

#     if user:
#         return user
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")



# @member_router.patch("/{user_uid}", response_model=User)
# async def update_user(user_uid: str, user_update_data: UserUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
#     updated_user = await user_service.update_user(user_uid, user_update_data, session)
        
#     if updated_user:
#         return updated_user
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


# @member_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(user_uid:str, session: AsyncSession = Depends(get_session)):
#     user_to_delete = await user_service.delete_user(user_uid, session)

#     if not user_to_delete:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

