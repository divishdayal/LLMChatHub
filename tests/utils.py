from sqlalchemy.orm import Session
from typing import Tuple

from src import models


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
