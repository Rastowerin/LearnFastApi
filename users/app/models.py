from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field
from pydantic import EmailStr

DATABASE_URL = "postgresql+asyncpg://dbuser:123@localhost:5432/mydb"


class Role(Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    username: str = Field(unique=True)
    email: EmailStr
    first_name: str
    last_name: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    hashed_password: str = Field()
    role: Role = Field(default=Role.USER)

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserPublic(UserBase):
    id: int
    role: Role
