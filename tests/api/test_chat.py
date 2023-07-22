from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils import create_chat, create_user


def test_chat_get(client: TestClient, db: Session):
    # create user
    user_obj = create_user(db)

    # create chat
    response = client.post(
        "/api_v1/chat",
        json={
            "message": "first message",
            "user_id": user_obj.id,
        },
    )
    assert response.status_code == 200, response.text
    chat_id = response.json()["chat_id"]

    response = client.get(f"/api_v1/{user_obj.id}/chat/{chat_id}")
    assert response.status_code == 200, response.text


def test_generate(client: TestClient, db: Session):
    pass


def test_delete(client: TestClient, db: Session):
    # create user
    user_obj = create_user(db)
    chat_id = create_chat(user_obj, client)

    response = client.delete(
        f"/api_v1/chat/{chat_id}",
    )
    assert response.status_code == 200, response.text
