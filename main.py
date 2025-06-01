#внешние импорты
import asyncio
from sqlalchemy.future import select
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, AsyncGenerator, List
from passlib.context import CryptContext 

# Импорты из локальных файлов
from schemas import UserCreate, UserOut
from database import SessionLocal, engine
from models import User, Base

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#какая-то странная функция
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password):
    return pwd_context.hash(password)

# создание юзера
@app.post("/users/", response_model=UserCreate)
async def create_user(name: str, password: str, db: AsyncSession = Depends(get_db)) -> Any:
    hashed_password = get_password_hash(password)
    new_user = User(name=name, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# чтение юзера 
@app.get("/users/", response_model=List[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()