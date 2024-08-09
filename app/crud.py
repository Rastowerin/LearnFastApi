from fastapi import Depends

from sqlmodel import select, Session

from app.database import get_db
from app.models import UserPublic, UserCreate, User


def get_all_users(session: Session) -> list[UserPublic]:
    query = select(User).order_by(User.id)
    result = session.execute(query)
    users = result.scalars().all()
    return [UserPublic.from_orm(user) for user in users]


def get_user(user_id: int, session: Session = Depends(get_db)) -> UserPublic:
    return session.query(User).filter(User.id == user_id).first()


def create_user(user_create: UserCreate, session: Session = Depends(get_db)) -> UserPublic:
    user = User(**user_create.dict(), hashed_password=user_create.password + '_hash')
    session.add(user)
    return user


def update_user(user_id: int, user: UserCreate, session: Session = Depends(get_db)) -> UserPublic:
    db_user = session.query(User).filter(User.id == user_id).first()
    [setattr(db_user, key, value) for key, value in user.dict()]
    return db_user


def delete_user(user_id: int, session: Session = Depends(get_db)) -> None:
    user = session.query(User).filter(User.id == user_id).first()
    session.delete(user)
