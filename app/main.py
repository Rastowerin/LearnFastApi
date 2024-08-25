import uvicorn
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exceptions import UserNotFoundException, UserAlreadyExistsException, BadRequestError
from app.middleware import BearerTokenAuthBackend
from app.users.endpoints import router as users_router
from app.auth.endpoints import router as auth_router


app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())

app.include_router(users_router)
app.include_router(auth_router)


@app.exception_handler(BadRequestError)
async def unicorn_exception_handler(request: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=exc.status,
        content={"message": str(exc)},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
