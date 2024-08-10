from fastapi import FastAPI
from users.app.endpoints import router

app = FastAPI()

app.include_router(router)
