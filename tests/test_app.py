import pytest
from httpx import AsyncClient
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

@pytest.mark.asyncio
async def test_signup_and_unregister_activity():
    # Arrange
    email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: Sign up
        signup_response = await ac.post(f"/activities/{activity}/signup?email={email}")
        # Assert
        assert signup_response.status_code == 200
        assert f"Signed up {email} for {activity}" in signup_response.json()["message"]

        # Act: Unregister
        unregister_response = await ac.delete(f"/activities/{activity}/unregister?email={email}")
        # Assert
        assert unregister_response.status_code == 200
        assert f"Removed {email} from {activity}" in unregister_response.json()["message"]

@pytest.mark.asyncio
async def test_signup_duplicate():
    # Arrange
    email = "duplicateuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: First signup
        await ac.post(f"/activities/{activity}/signup?email={email}")
        # Act: Duplicate signup
        response = await ac.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_unregister_nonexistent():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
