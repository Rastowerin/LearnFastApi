import os

from fastapi import Request, HTTPException
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt

from app.users.models import User

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


class CustomAuthenticationMiddleware(AuthenticationMiddleware):

    def __init__(self, app, on_error):
        super().__init__(self, app=app, on_error=on_error, backend=BearerTokenAuthBackend())


class BearerTokenAuthBackend(AuthenticationBackend):

    async def authenticate(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        if authorization:
            try:
                scheme, token = authorization.split()
                if scheme.lower() != "bearer":
                    raise HTTPException(status_code=401, detail="Invalid authentication scheme")
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                if payload is None:
                    raise HTTPException(status_code=401, detail="Invalid or expired token")
                user = User(**payload)
                return authorization, user
            except (ValueError, HTTPException):
                raise HTTPException(status_code=401, detail="Invalid authorization header")
        else:
            return None
