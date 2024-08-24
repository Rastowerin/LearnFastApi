import uvicorn
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from app.middleware import BearerTokenAuthBackend
from app.users.endpoints import router as users_router
from app.auth.endpoints import router as auth_router


app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())

app.include_router(users_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
