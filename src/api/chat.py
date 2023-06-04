from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import schemas
from src.api import deps
from src.models.chat import Chat

router = APIRouter()


@router.post(
    "/{user_id}/chat/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ChatResponse,
)
def generate(
    user_id: int,
    chat_id: int,
    db: Session = Depends(deps.get_db),
) -> schemas.ChatResponse:
    """
    generates a chat response
    """

    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    #TODO: generate response

    respone = ""

    return schemas.ChatResponse(response=respone)
