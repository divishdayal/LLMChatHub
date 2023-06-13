import traceback

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import schemas
from src.api import deps
from src.models.user import User

router = APIRouter()


@router.post(
    "/create",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseMessage,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
) -> schemas.ResponseMessage:
    """
    Create a new user
    """
    db_user = User(
        email=user.email,
        name=user.name,
        username=user.username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.ResponseMessage(
        message=f"User #{db_user.id} created successfully",
    )
