"""User tests."""
from datetime import date

import pytest
from httpx import AsyncClient

from app.models.acces_app import AccesApp
from app.models.user import User
from app.security.passwords import hash_password
from sqlalchemy.ext.asyncio import AsyncSession


async def create_test_user_and_login(
    client: AsyncClient,
    db_session: AsyncSession,
    email: str = "testuser@example.com",
) -> str:
    """Helper to create user and return access token."""
    user = User(
        email=email,
        prenom="Test",
        nom="User",
        date_naissance=date(1990, 1, 1),
        rue="123 Street",
        npa="1000",
        localite="City",
        tel="0123456789",
    )
    db_session.add(user)
    await db_session.flush()

    acces = AccesApp(
        email=email,
        password_hash=hash_password("Password123!"),
    )
    db_session.add(acces)
    await db_session.commit()

    response = await client.post(
        "/auth/login",
        json={"email": email, "password": "Password123!"},
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, db_session: AsyncSession):
    """Test getting current user profile."""
    access_token = await create_test_user_and_login(client, db_session)

    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["prenom"] == "Test"
    assert data["nom"] == "User"


@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient):
    """Test getting profile without authentication."""
    response = await client.get("/users/me")
    assert response.status_code == 403  # No credentials provided


@pytest.mark.asyncio
async def test_update_current_user(client: AsyncClient, db_session: AsyncSession):
    """Test updating current user profile."""
    access_token = await create_test_user_and_login(client, db_session)

    response = await client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "first_name": "Updated",
            "last_name": "Name",
            "rue": "456 New Street",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["prenom"] == "Updated"
    assert data["nom"] == "Name"
    assert data["rue"] == "456 New Street"


@pytest.mark.asyncio
async def test_update_current_user_partial(client: AsyncClient, db_session: AsyncSession):
    """Test partial update of user profile."""
    access_token = await create_test_user_and_login(client, db_session)

    response = await client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"first_name": "PartialUpdate"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["prenom"] == "PartialUpdate"
    assert data["nom"] == "User"  # Unchanged
