from typing import Tuple

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src import models
from src.models import User


def create_user(
    db: Session,
    username: str = "testuser",
    name: str = "Test User",
    email: str = "test@user.com",
) -> Tuple[dict, models.User]:
    user_obj = models.User(name=name, username=username, email=email)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return user_obj


def create_chat(user: User, client: TestClient):
    # create chat
    response = client.post(
        "/api_v1/chat",
        json={
            "message": "first message",
            "user_id": user.id,
        },
    )
    assert response.status_code == 200, response.text
    chat_id = response.json()["chat_id"]
    return chat_id
