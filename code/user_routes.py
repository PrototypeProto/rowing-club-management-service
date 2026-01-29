from typing import Optional, Union, Annotated
'''
    Optional[type(s)]
    Union() or (type | None)
    Annotated[type, "annotation textr"]
'''
from fastapi import FastAPI, Header, APIRouter
from fastapi import status
from fastapi.exceptions import HTTPException
from .data_types import User, RegistrationDate

router = APIRouter()
users = []

# @router.get("/", status_code=200 )
# async def welcome():
#     return "You have reached the API" 

# @router.get("/")
# async def get_headers(
#     accept: str = Header(None),
#     content_type: str = Header(None),
#     user_agent: str = Header(None),
#     host: str = Header(None)
# ):
#     request_headers = {}
    
#     request_headers["Accept"] = accept
#     request_headers["Content-Type"] = content_type
#     request_headers["User-Agent"] = user_agent
#     request_headers["Host"] = host

#     return request_headers


@router.post("/")
async def insertUser(user: User):
    users.append(user)

    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="uhh")
    return users


@router.get("/")
async def bad_access(user: User):

    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="uhh")


@router.patch("/")
async def update(user: User):
    
    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="uhh")
        
    return 2

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user: User):
    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="uhh")

    return 3