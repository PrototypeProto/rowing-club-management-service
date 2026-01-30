from typing import Optional, Union, Annotated
'''
    Optional[type(s)]
    Union() or (type | None)
    Annotated[type, "annotation textr"]
'''
from fastapi import FastAPI, Header, APIRouter
from fastapi import status
from fastapi.exceptions import HTTPException
from .data_types import Users

router_at_users = APIRouter()




@router_at_users.post("/")
async def insertUser(user: Users):

    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="uhh")
    return users


@router_at_users.get("/")
async def bad_access():

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="uhh")


@router_at_users.patch("/")
async def update(user: Users):
    
    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="uhh")
        
    return 2

@router_at_users.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user: Users):
    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="uhh")

    return 3