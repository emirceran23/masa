"""Unit tests for auth endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthRegister:
    async def test_register_success(self, client: AsyncClient):
        resp = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@lagent.dev",
                "password": "SecurePass123!@#",
                "full_name": "New User",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "newuser@lagent.dev"
        assert "id" in data

    async def test_register_weak_password(self, client: AsyncClient):
        resp = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "weak@lagent.dev",
                "password": "short",
                "full_name": "Weak User",
            },
        )
        assert resp.status_code == 422  # validation error from schema (min_length=12)

    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        resp = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@lagent.dev",  # already exists
                "password": "AnotherPass123!@#",
                "full_name": "Dup User",
            },
        )
        assert resp.status_code == 409


@pytest.mark.asyncio
class TestAuthLogin:
    async def test_login_success(self, client: AsyncClient, test_user):
        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@lagent.dev", "password": "TestPass123!@#"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@lagent.dev", "password": "WrongPassword123!@"},
        )
        assert resp.status_code == 401

    async def test_login_nonexistent_user(self, client: AsyncClient):
        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "ghost@lagent.dev", "password": "SomePass123!@#"},
        )
        assert resp.status_code == 401


@pytest.mark.asyncio
class TestAuthMe:
    async def test_me_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    async def test_me_authenticated(self, client: AsyncClient, test_user):
        # Login first
        login_resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@lagent.dev", "password": "TestPass123!@#"},
        )
        token = login_resp.json()["access_token"]

        resp = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["email"] == "test@lagent.dev"
