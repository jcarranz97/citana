import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.auth.models import User
from app.auth.utils import get_password_hash
from app.database import Base, get_db
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://citana_user:citana_password@localhost:5433/citana_test_db",
)

engine_test = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

ADMIN_USERNAME = "test-admin"
ADMIN_PASSWORD = "test-admin-pass"
USER_USERNAME = "test-user"
USER_PASSWORD = "test-user-pass"


@pytest.fixture
def db() -> Generator[Session]:
    Base.metadata.create_all(bind=engine_test)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client(db: Session) -> Generator[TestClient]:
    def override_get_db() -> Generator[Session]:
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_admin(db: Session) -> User:
    user = User(
        username=ADMIN_USERNAME,
        password_hash=get_password_hash(ADMIN_PASSWORD),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user(db: Session) -> User:
    user = User(
        username=USER_USERNAME,
        password_hash=get_password_hash(USER_PASSWORD),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_auth_headers(
    client: TestClient, username: str, password: str
) -> dict[str, str]:
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
