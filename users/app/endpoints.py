from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from users.app.database import get_db
from users.app.models import UserCreate, UserPublic, UserUpdate
from users.app import service

router = APIRouter()


@router.get("/users", response_model=list[UserPublic], status_code=200)
async def get_all_users(session: AsyncSession = Depends(get_db)):
    return await service.get_all_users(session)


@router.get("/users/{id}", response_model=UserPublic, status_code=200)
async def get_user(id: int, session: AsyncSession = Depends(get_db)):
    return await service.get_user(session, id)


@router.post("/users", response_model=UserPublic, status_code=201)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await service.create_user(session, user)


@router.patch("/users/{id}", response_model=UserPublic, status_code=200)
async def update_user(id: int, user: UserUpdate, session: AsyncSession = Depends(get_db)):
    return await service.update_user(session, id, user)


@router.delete("/users/{id}", status_code=204)
async def delete_user(id: int, session: AsyncSession = Depends(get_db)):
    await service.delete_user(session, id)
