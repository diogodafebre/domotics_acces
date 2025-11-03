"""Authentication tests."""
from datetime import date

import pytest
from httpx import AsyncClient

from app.models.acces_app import AccesApp
from app.models.user import User
from app.security.passwords import hash_password
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Test successful user registration."""
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
            "date_naissance": "1990-01-01",
            "rue": "123 Test Street",
            "npa": "1000",
            "localite": "TestCity",
            "tel": "0123456789",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["prenom"] == "Test"
    assert data["nom"] == "User"
    assert "user_id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, db_session: AsyncSession):
    """Test registration with duplicate email."""
    # Create existing user
    user = User(
        email="existing@example.com",
        prenom="Existing",
        nom="User",
        date_naissance=date(1990, 1, 1),
        rue="123 Street",
        npa="1000",
        localite="City",
    )
    db_session.add(user)
    await db_session.commit()

    # Try to register with same email
    response = await client.post(
        "/auth/register",
        json={
            "email": "existing@example.com",
            "password": "Password123!",
            "first_name": "Test",
            "last_name": "User",
            "date_naissance": "1990-01-01",
            "rue": "123 Test Street",
            "npa": "1000",
            "localite": "TestCity",
        },
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db_session: AsyncSession):
    """Test successful login."""
    # Create test user
    user = User(
        email="login@example.com",
        prenom="Login",
        nom="User",
        date_naissance=date(1990, 1, 1),
        rue="123 Street",
        npa="1000",
        localite="City",
    )
    db_session.add(user)
    await db_session.flush()

    acces = AccesApp(
        email="login@example.com",
        password_hash=hash_password("Password123!"),
    )
    db_session.add(acces)
    await db_session.commit()

    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    response = await client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, db_session: AsyncSession):
    """Test token refresh."""
    # Create and login user
    user = User(
        email="refresh@example.com",
        prenom="Refresh",
        nom="User",
        date_naissance=date(1990, 1, 1),
        rue="123 Street",
        npa="1000",
        localite="City",
    )
    db_session.add(user)
    await db_session.flush()

    acces = AccesApp(
        email="refresh@example.com",
        password_hash=hash_password("Password123!"),
    )
    db_session.add(acces)
    await db_session.commit()

    login_response = await client.post(
        "/auth/login",
        json={
            "email": "refresh@example.com",
            "password": "Password123!",
        },
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh token
    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_logout(client: AsyncClient, db_session: AsyncSession):
    """Test logout."""
    # Create and login user
    user = User(
        email="logout@example.com",
        prenom="Logout",
        nom="User",
        date_naissance=date(1990, 1, 1),
        rue="123 Street",
        npa="1000",
        localite="City",
    )
    db_session.add(user)
    await db_session.flush()

    acces = AccesApp(
        email="logout@example.com",
        password_hash=hash_password("Password123!"),
    )
    db_session.add(acces)
    await db_session.commit()

    login_response = await client.post(
        "/auth/login",
        json={
            "email": "logout@example.com",
            "password": "Password123!",
        },
    )
    refresh_token = login_response.json()["refresh_token"]

    # Logout
    response = await client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 204

    # Try to use refresh token after logout (should fail)
    refresh_response = await client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_response.status_code == 401
