#внешние импорты
import asyncio
from sqlalchemy.future import select
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, AsyncGenerator

# Импорты из локальных файлов
from schemas import UserCreate, UserOut
from database import SessionLocal, engine
from models import User, Base

app = FastAPI()

# это код инициализирует базу данных 
async def init_db():  # создаётся ф-ия для инициализации БД
    async with engine.begin() as conn:  # открывается контекст менеджер, создаётся транзакция и подключение к БД
        await conn.run_sync(Base.metadata.create_all)

#какая-то странная функция
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# создание юзера
@app.post("/users/", response_model=UserCreate)
async def create_user(name: str, password: str, AsyncSession = Depends(get_db)) -> Any:
    new_user = User(name=name, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# чтение юзера 
@app.get("/users/", response_model=UserOut)
async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()