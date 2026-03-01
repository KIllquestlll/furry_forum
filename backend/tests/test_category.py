import pytest
from httpx import AsyncClient,ASGITransport

from unittest.mock import patch,AsyncMock

# Import package
from app.service.user.authService import get_current_user
from app.schemas.user.userScheme import UserRead
from .conftest import override_get_current_admin,override_get_current_user,BASE_URL_TEST
from app.main import app

# Checked func on show all categoryes 
async def test_get_all_categories_success(ac,mocker):
    mock_data = [{"id":1,"title":"furry"},{"id":2,"title":"pony"}]

    mocker.patch("app.api.category.GettingAllCategory",
                 return_value=mock_data)

    response = await ac.get("/api/category/show")

    assert response.status_code == 200
    assert response.json() == mock_data

    print(f"{response.json()}")


# Test on created category user witch have role admin
async def test_create_category(mocker):

    async def override_get_current_user():
        return UserRead(
            id=2,
            username="admin",
            email="123@gmail.com",
            role_title="admin",
            is_banned=False
        )
    
    app.dependency_overrides[get_current_user] = override_get_current_admin
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport,base_url="http://test") as ac:
        headers  = {"Authorization":"Bearer secret-token"}
        payload  = {"title":"fdfdg"}

        response = await ac.post("/api/category/create",
                                 json=payload,
                                 headers=headers)
        
        app.dependency_overrides.clear()

        assert response.status_code == 200


# POST-TEST
# Test func on created category user witch have role user
async def test_create_category_forbiden():

    async def override_get_current_user():
        return UserRead(
            id=2,
            username="guess",
            email="123@gmail.com",
            role_title="user",
            is_banned=False
        )
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport,base_url="http://test") as ac:
        headers  = {"Authorization":"Bearer secret-token"}
        payload  = {"title":"53453443243246"}

        response = await ac.post("/api/category/create",
                                 json=payload,
                                 headers=headers)
        
        app.dependency_overrides.clear()

        assert response.status_code == 403


# Test on created category that almost created
async def test_create_category_repeat():

    
    app.dependency_overrides[get_current_user] = override_get_current_admin
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport,base_url="http://test") as ac:
        headers  = {"Authorization":"Bearer secret-token"}
        payload  = {"title":"53453443243246"}

        response = await ac.post("/api/category/create",
                                 json=payload,
                                 headers=headers)
        
        app.dependency_overrides.clear()

        assert response.status_code == 400


# DELETE-TEST
async def test_delete_category_all(ac):

    app.dependency_overrides[get_current_user] = override_get_current_admin
    
    try:
        header = {"Authorization":"Bearer secret-token"}

        response =  await ac.delete("/api/category/delete/category")
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()