import pytest

@pytest.mark.asyncio
async def test_get_activities(client):
    # Arrange: cliente ya viene del fixture
    # Act
    response = await client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_signup_and_unregister_activity(client):
    email = "pytestuser@mergington.edu"
    activity = "Chess Club"

    # Act: signup
    response = await client.post("/signup", json={"email": email, "activity": activity})
    # Assert
    assert response.status_code == 200

    # Act: unregister
    response = await client.post("/unregister", json={"email": email, "activity": activity})
    # Assert
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_signup_duplicate(client):
    email = "duplicateuser@mergington.edu"
    activity = "Chess Club"

    # Act: primer registro
    response = await client.post("/signup", json={"email": email, "activity": activity})
    # Assert
    assert response.status_code == 200

    # Act: intento duplicado
    response = await client.post("/signup", json={"email": email, "activity": activity})
    # Assert
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_unregister_nonexistent(client):
    email = "notfound@mergington.edu"
    activity = "Chess Club"

    # Act
    response = await client.post("/unregister", json={"email": email, "activity": activity})
    # Assert
    assert response.status_code == 404
