from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_chat_get(client: TestClient, db: Session):
    response = client.get("/api_v1/1/chat/1")
    assert response.status_code == 404

def test_generate(client: TestClient, db: Session):
    pass