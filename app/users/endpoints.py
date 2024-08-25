from fastapi import APIRouter, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_db
from app.users.models import UserCreate, UserPublic, UserUpdate
from app.users.services import get_user, get_all_users, create_user, update_user, delete_user

router = APIRouter()


@router.get("/users", response_model=list[UserPublic], status_code=200)
async def get_list(session: AsyncSession = Depends(get_db)):
    return await get_all_users(session)


@router.get("/users/{id}", response_model=UserPublic, status_code=200)
async def get_detail(id: int, session: AsyncSession = Depends(get_db)):
    return await get_user(session, id)


@router.post("/users", response_model=UserPublic, status_code=201)
async def post(user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await create_user(session, user)


@router.patch("/users/{id}", response_model=UserPublic, status_code=200)
async def patch(id: int, user: UserUpdate, session: AsyncSession = Depends(get_db)):
    return await update_user(session, id, user)


@router.delete("/users/{id}", status_code=204)
async def delete(id: int, session: AsyncSession = Depends(get_db)):
    await delete_user(session, id)
