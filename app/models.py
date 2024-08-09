from enum import Enum

from sqlmodel import SQLModel, Field
from pydantic import EmailStr

DATABASE_URL = "postgresql://dbuser:123@localhost:5432/mydb"


class Role(Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    username: str
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


class UserPublic(UserBase):
    id: int
    role: Role
