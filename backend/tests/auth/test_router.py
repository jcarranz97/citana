from fastapi.testclient import TestClient

from app.auth.models import User
from tests.conftest import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    USER_PASSWORD,
    USER_USERNAME,
    get_auth_headers,
)


class TestLogin:
    def test_login_success(self, client: TestClient, test_user: User) -> None:
        resp = client.post(
            "/api/v1/auth/login",
            data={"username": USER_USERNAME, "password": USER_PASSWORD},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["access_token"]
        assert body["token_type"] == "Bearer"
        assert body["expires_in"] > 0

    def test_login_bad_credentials(self, client: TestClient, test_user: User) -> None:
        resp = client.post(
            "/api/v1/auth/login",
            data={"username": USER_USERNAME, "password": "wrong"},
        )
        assert resp.status_code == 401


class TestMe:
    def test_me_requires_auth(self, client: TestClient) -> None:
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_me_returns_self(self, client: TestClient, test_user: User) -> None:
        headers = get_auth_headers(client, USER_USERNAME, USER_PASSWORD)
        resp = client.get("/api/v1/auth/me", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["username"] == USER_USERNAME


class TestRegister:
    def test_register_requires_admin(self, client: TestClient, test_user: User) -> None:
        headers = get_auth_headers(client, USER_USERNAME, USER_PASSWORD)
        resp = client.post(
            "/api/v1/auth/register",
            json={"username": "new-user", "password": "password123"},
            headers=headers,
        )
        assert resp.status_code == 403

    def test_admin_can_register(self, client: TestClient, test_admin: User) -> None:
        headers = get_auth_headers(client, ADMIN_USERNAME, ADMIN_PASSWORD)
        resp = client.post(
            "/api/v1/auth/register",
            json={"username": "new-user", "password": "password123"},
            headers=headers,
        )
        assert resp.status_code == 201
        assert resp.json()["username"] == "new-user"

    def test_duplicate_username_returns_409(
        self, client: TestClient, test_admin: User, test_user: User
    ) -> None:
        headers = get_auth_headers(client, ADMIN_USERNAME, ADMIN_PASSWORD)
        resp = client.post(
            "/api/v1/auth/register",
            json={"username": USER_USERNAME, "password": "password123"},
            headers=headers,
        )
        assert resp.status_code == 409
