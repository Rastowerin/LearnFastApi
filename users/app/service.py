from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from users.app.models import UserPublic, UserCreate, User, UserUpdate


async def get_all_users(session: AsyncSession) -> list[UserPublic]:
    query = select(User).order_by(User.id)
    result = await session.exec(query)
    users = result.all()
    return [UserPublic.from_orm(user) for user in users]


async def get_user(session: AsyncSession, user_id: int) -> UserPublic:
    query = select(User).where(User.id == user_id)
    result = await session.exec(query)
    user = result.first()
    return UserPublic.from_orm(user)


async def create_user(session: AsyncSession, user: UserCreate) -> UserPublic:
    db_user = User(**user.dict(), hashed_password=user.password + '_hashed')
    session.add(db_user)
    query = select(User).where(User.username == db_user.username)
    result = await session.exec(query)
    user = result.first()
    return UserPublic.from_orm(user)


async def update_user(session: AsyncSession, user_id: int, user: UserUpdate) -> UserPublic:
    query = select(User).filter(User.id == user_id)
    result = await session.exec(query)
    db_user = result.first()
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.add(db_user)
    return UserPublic.from_orm(db_user)


async def delete_user(session: AsyncSession, user_id: int) -> None:
    query = select(User).filter(User.id == user_id)
    result = await session.exec(query)
    db_user = result.first()
    await session.delete(db_user)
    return
