from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.user import User


def test_create_user(client: TestClient, db: Session):
    response = client.post(
        "/api_v1/user/create",
        json={
            "email": "test@user.com",
            "name": "Test User",
            "username": "testuser",
        },
    )
    assert response.status_code == 200, response.text
    assert db.query(User).filter(User.email == "test@user.com").count() == 1
