from sqlmodel import SQLModel


class UserCredentials(SQLModel):
    username: str
    password: str
