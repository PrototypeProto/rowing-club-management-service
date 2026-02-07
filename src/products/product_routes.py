from typing import Optional, Union, Annotated, List
'''
    Optional[type(s)]
    Union() or (type | None)
    Annotated[type, "annotation textr"]
'''
from fastapi import FastAPI, Header, APIRouter, Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from .schemas import ProductUpdateModel, ProductCreateModel, Product
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ProductService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer

'''
    A custom route to access products
    simple CRUD routes
    calls service() methods to perform business logic
'''

router_at_products = APIRouter()
product_service = ProductService()
access_token_bearer = AccessTokenBearer()


@router_at_products.post("/", response_model=Product)
async def create_product(product_data: ProductCreateModel, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)) -> dict:
    try:
        new_product = await product_service.create_product(product_data, session)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="failed to create product")

    return new_product


@router_at_products.get("/all", response_model=List[Product])
async def get_all_products(session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    products = await product_service.get_all_products(session)
    return products

@router_at_products.get("/{product_uid}", response_model=Product)
async def get_product(product_uid: str, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)) -> dict:
    product = await product_service.get_product(product_uid, session)

    if product:
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")



@router_at_products.patch("/{product_uid}", response_model=Product)
async def update_product(product_uid: str, product_update_data: ProductUpdateModel, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)) -> dict:
    updated_product = await product_service.update_product(product_uid, product_update_data, session)
        
    if updated_product:
        return updated_product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")


@router_at_products.delete("/{product_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_uid:str, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    product_to_delete = await product_service.delete_product(product_uid, session)

    if not product_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
