from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from ..code.config import Config


engine = AsyncEngine(
    create_engine(
        url=Config.DB_URL,
        echo=True
))

async def init_db():
    async with engine.begin() as conn:
        from ..code.data_types import Users

        await conn.run_sync(SQLModel.metadata.create_all)