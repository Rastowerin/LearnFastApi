import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.testclient import TestClient

from app import get_db
from app import app


DATABASE_URL_TEST = 'sqlite+aiosqlite:///:memory:'

async_engine = create_async_engine(DATABASE_URL_TEST)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

DATABASE_URL_TEST = 'sqlite+aiosqlite:///:memory:'

engine = create_async_engine(DATABASE_URL_TEST)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope='session')
def client():
    async def override_get_db() -> AsyncSession:
        async with AsyncSessionLocal() as session:
            yield session
            await session.commit()
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


@pytest.fixture(scope='function')
async def reset():

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
