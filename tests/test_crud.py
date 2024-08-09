from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.main import app
from app.models import DATABASE_URL

DATABASE_URL_TEST = DATABASE_URL + '_test'
engine = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


def test_create_user():

    data = {
        "username": "a",
        "first_name": "a",
        "last_name": "a",
        "email": "a@mail.com",
        "password": "1"
    }

    response = client.post("/users", json=data)
    assert response.status_code == 201
    result = response.json()
    del result["id"]

    expected = {
        **data,
        'role': 'user',
        'hashed_password': '1_hash'
    }
    del expected['password']

    assert result == expected
