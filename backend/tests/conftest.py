# Connection main library
from httpx import AsyncClient,ASGITransport
import pytest

# Import package
from app.main import app
from app.schemas.user.userScheme import UserRead

BASE_URL_TEST = "http://test"


@pytest.fixture()
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url=BASE_URL_TEST) as client:
        yield client
        
async def override_get_current_user():
        return UserRead(
            id=2,
            username="guess",
            email="123@gmail.com",
            role_title="user",
            is_banned=False
        )

async def override_get_current_admin():
        return UserRead(
            id=2,
            username="guess",
            email="123@gmail.com",
            role_title="admin",
            is_banned=False
        )