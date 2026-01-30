from typing import Optional, Union, Annotated
'''
    Optional[type(s)]
    Union() or (type | None)
    Annotated[type, "annotation textr"]
'''
from fastapi import FastAPI, Header, APIRouter
from fastapi import status
from fastapi.exceptions import HTTPException
# from .data_types import Users

router_at_root = APIRouter()
users = []

@router_at_root.get("/", status_code=200 )
async def welcome():
    return "You have reached the API" 

@router_at_root.get("/")
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
):
    request_headers = {}
    
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers

