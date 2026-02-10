from typing import Optional, Union, Annotated
'''
    Optional[type(s)]
    Union() or (type | None)
    Annotated[type, "annotation textr"]
'''
from fastapi import FastAPI, Header
from src.auth.user_routes import router_at_users
from src.products.product_routes import router_at_products
from src.root_routes import router_at_root
from src.config import Settings
from src.db.main import init_db

from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...")
    
    # If we want to autogenerate the DB based on our SQLModels
    # Using Alembic instead to manage DB updates
    await init_db()
    
    yield
    print("Server has been stopped...")

# api_version = "v1"
# s = Settings()
# print(s.DB_URL)

# app = FastAPI(version=api_version)
app = FastAPI(
    title="userManager",
    description="manage users",
    # lifespan=life_span
)

# app.include_router(router=router, prefix=f"/{api_version}/user")
app.include_router(router=router_at_users, prefix="/auth")
app.include_router(router=router_at_root, prefix="")
app.include_router(router=router_at_products, prefix="/products")
