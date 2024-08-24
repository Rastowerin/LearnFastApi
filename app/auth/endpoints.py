from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.services import generate_token
from app.database import get_db
from app.auth.models import UserCredentials
from app.exceptions import UserNotFoundException, InvalidCredentialsException

router = APIRouter()


@router.post("/login", status_code=200)
async def login(credentials: UserCredentials, session: AsyncSession = Depends(get_db)):
    try:
        return {"token": await generate_token(session, credentials)}
    except (UserNotFoundException, InvalidCredentialsException) as e:
        code = {
            UserNotFoundException: 404,
            InvalidCredentialsException: 401
        }[type(e)]
        raise HTTPException(detail=str(e), status_code=code)
