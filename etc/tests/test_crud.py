import pytest


user_data1 = {
    "username": "qwerty",
    "first_name": "Alex",
    "last_name": "Jonson",
    "email": "alex@mail.com",
    "password": "Abg%sad12@s"
}


user_data2 = {
    "username": "qwerty123",
    "first_name": "Sanya",
    "last_name": "Ivanov",
    "email": "kuraga@mail.com",
    "password": "aJ7Nb(*a"
}

user_data1_update = {
    "username": "ytrewq",
}


@pytest.mark.asyncio
async def test_create(client, reset):
    await reset

    response = client.post('/users', json=user_data1)
    assert response.status_code == 201

    result = response.json()
    del result['id']

    expected = {
        **user_data1,
        'role': 'user'
    }
    del expected['password']

    assert result == expected


@pytest.mark.asyncio
async def test_get_single(client, reset):
    await reset

    response = client.post('/users', json=user_data1)
    id = response.json()['id']

    response = client.get(f'/users/{id}')
    assert response.status_code == 200

    result = response.json()
    del result['id']

    expected = {
        **user_data1,
        'role': 'user'
    }
    del expected['password']

    assert result == expected


@pytest.mark.asyncio
async def test_get_all(client, reset):
    await reset

    client.post('/users', json=user_data1)
    client.post('/users', json=user_data2)

    response = client.get('/users')
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2


@pytest.mark.asyncio
async def test_update(client, reset):
    await reset

    response = client.post('/users', json=user_data1)
    id = response.json()['id']

    response = client.patch(f'/users/{id}', json=user_data1_update)
    assert response.status_code == 200

    result = response.json()

    expected = {
        'id': id,
        **user_data1,
        **user_data1_update,
        'role': 'user',
    }
    del expected['password']

    assert result == expected


@pytest.mark.asyncio
async def test_delete(client, reset):
    await reset

    response = client.post('/users', json=user_data1)
    id = response.json()['id']

    response = client.delete(f'/users/{id}')
    assert response.status_code == 204

    response = client.get(f'/users')

    result = response.json()
    expected = []

    assert result == expected
