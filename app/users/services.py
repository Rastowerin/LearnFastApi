from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.users.models import UserCreate, User, UserUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_all_users(session: AsyncSession) -> list[User]:
    query = select(User).order_by(User.id)
    result = await session.exec(query)
    users = list(result.all())
    return users


async def get_user(session: AsyncSession, user_id: int) -> User:
    query = select(User).where(User.id == user_id)
    result = await session.exec(query)
    user = result.first()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    query = select(User).where(User.username == username)
    result = await session.exec(query)
    user = result.first()
    return user


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    hashed_password = pwd_context.hash(user_create.password)
    user = User(**user_create.model_dump(), hashed_password=hashed_password)
    session.add(user)
    query = select(User).where(User.username == user.username)
    result = await session.exec(query)
    user = result.first()
    return user


async def update_user(session: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
    query = select(User).filter(User.id == user_id)
    result = await session.exec(query)
    user = result.first()
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    query = select(User).filter(User.id == user_id)
    result = await session.exec(query)
    user = result.first()
    await session.delete(user)
