from fastapi import FastAPI
from endpoints import router
import mq_listener

app = FastAPI()

app.include_router(router)
