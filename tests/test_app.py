import pytest
from httpx import AsyncClient
from src.app import app

import asyncio

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_successful_signup():
    # Arrange
    test_email = "testuser1@mergington.edu"
    activity = "Art Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {test_email} for {activity}" in response.json()["message"]
    # Cleanup
    await ac.delete(f"/activities/{activity}/signup?email={test_email}")

@pytest.mark.asyncio
async def test_duplicate_signup():
    # Arrange
    test_email = "testuser2@mergington.edu"
    activity = "Drama Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        await ac.post(f"/activities/{activity}/signup?email={test_email}")
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    await ac.delete(f"/activities/{activity}/signup?email={test_email}")

@pytest.mark.asyncio
async def test_unregister_participant():
    # Arrange
    test_email = "testuser3@mergington.edu"
    activity = "Science Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(f"/activities/{activity}/signup?email={test_email}")
        # Act
        response = await ac.delete(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {test_email} from {activity}" in response.json()["message"]

@pytest.mark.asyncio
async def test_unregister_nonexistent_participant():
    # Arrange
    test_email = "notregistered@mergington.edu"
    activity = "Debate Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.delete(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]
