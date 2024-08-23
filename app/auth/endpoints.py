from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_db
from app.auth.models import UserCredentials
from app.users.services import get_all_users

router = APIRouter()


@router.post("/login", status_code=200)
async def login(credentials: UserCredentials, session: AsyncSession = Depends(get_db)):
    user = get
    return await get_all_users(session)
