from fastapi.testclient import TestClient
from app.api.main import app
from app.adapters.repositories.base import SessionLocal
from app.core.models.user import User
from app.core.services.auth_service import create_access_token, get_password_hash
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(db):
    username = "testuser"
    password = "testpassword"
    hashed_password = get_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()

@pytest.fixture
def test_token(test_user):
    access_token = create_access_token(data={"sub": test_user.username})
    return access_token

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_register_user(db):
    response = client.post(
        "/auth/register", json={"username": "newuser", "password": "newpassword"}
    )
    assert response.status_code == 200

def test_login_user(test_user):
    response = client.post(
        "/auth/login", json={"username": test_user.username, "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_read_users_me(test_token):
    response = client.get(
        "/auth/me", headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200

def test_create_task(test_token):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"title": "Test Task"},
    )
    assert response.status_code == 200
