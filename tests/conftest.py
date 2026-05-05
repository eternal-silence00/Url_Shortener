import pytest
from app.main import app
from httpx import AsyncClient, ASGITransport

@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client