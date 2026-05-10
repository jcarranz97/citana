from fastapi.testclient import TestClient

from app.auth.models import User
from tests.conftest import USER_PASSWORD, USER_USERNAME, get_auth_headers

from .conftest import future_iso


class TestListAppointments:
    def test_requires_auth(self, client: TestClient) -> None:
        resp = client.get("/api/v1/appointments/")
        assert resp.status_code == 401

    def test_empty_list(self, client: TestClient, test_user: User) -> None:
        headers = get_auth_headers(client, USER_USERNAME, USER_PASSWORD)
        resp = client.get("/api/v1/appointments/", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == []


class TestCreateAppointment:
    def test_happy_path(self, client: TestClient, test_user: User) -> None:
        headers = get_auth_headers(client, USER_USERNAME, USER_PASSWORD)
        payload = {
            "customer_name": "Jane Doe",
            "customer_phone": "+15551234567",
            "start_time": future_iso(48),
            "duration_minutes": 30,
            "notes": "First-time customer",
        }
        resp = client.post("/api/v1/appointments/", json=payload, headers=headers)
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["status"] == "pending"
        assert body["customer_phone"] == "+15551234567"
        assert body["duration_minutes"] == 30

    def test_past_start_time_rejected(
        self, client: TestClient, test_user: User
    ) -> None:
        headers = get_auth_headers(client, USER_USERNAME, USER_PASSWORD)
        payload = {
            "customer_name": "Jane Doe",
            "customer_phone": "+15551234567",
            "start_time": future_iso(-1),
            "duration_minutes": 30,
        }
        resp = client.post("/api/v1/appointments/", json=payload, headers=headers)
        assert resp.status_code == 422

    def test_invalid_phone_rejected(self, client: TestClient, test_user: User) -> None:
        headers = get_auth_headers(client, USER_USERNAME, USER_PASSWORD)
        payload = {
            "customer_phone": "abc",
            "start_time": future_iso(48),
            "duration_minutes": 30,
        }
        resp = client.post("/api/v1/appointments/", json=payload, headers=headers)
        assert resp.status_code == 422


class TestCancelAppointment:
    def test_cancel_sets_status_cancelled(
        self, client: TestClient, test_user: User
    ) -> None:
        headers = get_auth_headers(client, USER_USERNAME, USER_PASSWORD)
        create_resp = client.post(
            "/api/v1/appointments/",
            json={
                "customer_phone": "+15551234567",
                "start_time": future_iso(48),
                "duration_minutes": 30,
            },
            headers=headers,
        )
        assert create_resp.status_code == 201
        appt_id = create_resp.json()["id"]

        cancel_resp = client.delete(f"/api/v1/appointments/{appt_id}", headers=headers)
        assert cancel_resp.status_code == 200
        assert cancel_resp.json()["status"] == "cancelled"

    def test_get_unknown_returns_404(self, client: TestClient, test_user: User) -> None:
        headers = get_auth_headers(client, USER_USERNAME, USER_PASSWORD)
        resp = client.get(
            "/api/v1/appointments/00000000-0000-0000-0000-000000000000",
            headers=headers,
        )
        assert resp.status_code == 404
