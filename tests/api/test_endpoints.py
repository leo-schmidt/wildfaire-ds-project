import pytest
import numpy as np
from httpx import AsyncClient
import os

# test input is an array of shape 64x64x12 like the real input later
test_input = {
                'data' : np.zeros((64,64,12), dtype=np.uint8).tolist()
                }

@pytest.mark.asyncio
async def test_root_is_up():
    from wildfaire.api.fast import app
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_root_returns_greeting():
    from wildfaire.api.fast import app
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/")
    assert response.json() == {'greeting': "Hello, this is the landing page for the WildfAIre API."}


@pytest.mark.asyncio
async def test_predict_is_up():
    from wildfaire.api.fast import app
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/predict", json=test_input)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_predict_is_dict():
    from wildfaire.api.fast import app
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/predict", json=test_input)
    assert isinstance(response.json(), dict)
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_predict_has_key():
    from wildfaire.api.fast import app
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/predict", json=test_input)
    assert response.json().get('fire_spread', False)


@pytest.mark.asyncio
async def test_predict_val_is_float():
    from wildfaire.api.fast import app
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/predict", json=test_input)
    assert isinstance(response.json().get('fire_spread'), list)

@pytest.mark.asyncio
async def test_predict_image_is_up():
    from wildfaire.api.fast import app
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/predict_image", json=test_input)
    assert response.status_code == 200
