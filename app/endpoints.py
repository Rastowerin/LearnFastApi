from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlmodel import Session

from app.database import get_db
from app.models import UserCreate, UserPublic
from app import crud

router = APIRouter()


@router.get("/users", response_model=list[UserPublic], status_code=200)
async def get_all_users(session: Session = Depends(get_db)):
    return crud.get_all_users(session)


@router.get("/users/{id}", response_model=UserPublic, status_code=200)
async def get_user(id: int, session: Session = Depends(get_db)):
    user = crud.get_user(id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=None, status_code=201)
async def create_user(user: UserCreate, session: Session = Depends(get_db)):
    user = crud.create_user(user, session)
    return user


@router.patch("/users/{id}", response_model=None, status_code=201)
async def update_user(id: int, user: UserCreate, session: Session = Depends(get_db)):
    crud.update_user(id, user, session)


@router.delete("/users/{id}", response_model=None, status_code=204)
async def delete_user(id: int, session: Session = Depends(get_db)):
    try:
        crud.delete_user(id, session)
    except UnmappedInstanceError:
        return HTTPException(status_code=404, detail="User not found")
