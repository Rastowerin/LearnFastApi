from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from dotenv import load_dotenv
import os

from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.models import UserCredentials
from app.exceptions import InvalidCredentialsException
from app.users.services import get_user_by_username

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def generate_token(session: AsyncSession, credentials: UserCredentials) -> str:
    user = await get_user_by_username(session, credentials.username)

    if not user or not pwd_context.verify(hash=user.hashed_password, secret=credentials.password):
        raise InvalidCredentialsException("Invalid credentials")

    to_encode = {
        **user.model_dump(),
        'role': str(user.role),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# pwd_context.verify(plain_password, hashed_password)
#
# pwd_context.hash(password)
#
# encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
# payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
