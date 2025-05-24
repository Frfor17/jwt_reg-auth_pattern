import asyncio
from sqlalchemy.future import select
from database import SessionLocal, engine
from models import User, Base
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# это код инициализирует базу данных 
async def init_db():  # создаётся ф-ия для инициализации БД
    async with engine.begin() as conn:  # открывается контекст менеджер, создаётся транзакция и подключение к БД
        await conn.run_sync(Base.metadata.create_all)

# создание юзера
async def create_user(db: AsyncSession, user_id: int)
    new_user = User(name=name, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# чтение юзера 
async def get_all_users(db: AsyncSession)
    result = await db.execute(select(User))
    return result.scalars().all()