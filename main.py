import asyncio
from sqlalchemy.future import select
from database import SessionLocal, engine
from models import User, Base
from fastapi import FastAPI

app = FastAPI()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)