# models.py
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

pwd_context.verify(plain_password, hashed_password)

pwd_context.hash(password)

encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
