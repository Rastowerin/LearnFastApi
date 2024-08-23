from contextlib import asynccontextmanager

import aio_pika
import uvicorn
from fastapi import FastAPI

from app.users.endpoints import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rabbit_connection = await aio_pika.connect_robust("amqp://guest:guest@localhost:5672/")
    app.state.rabbit_channel = await app.state.rabbit_connection.channel()
    yield
    await app.state.rabbit_connection.close()


async def consume_messages():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost:5672/")
    async with connection:
        channel = await connection.channel()
        async for message in channel:
            async with message.process():
                print(f"Received message: {message.body.decode()}")

app = FastAPI(lifespan=None)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
