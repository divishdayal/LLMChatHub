import traceback

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import schemas
from src.api import deps
from src.models.chat import Chat, Message
from src.services.chatbot import ChatBot

router = APIRouter()


@router.get(
    "/{user_id}/chat/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ChatMessages,
)
def get_chat(
    chat_id: int,
    user_id: int,
    db: Session = Depends(deps.get_db),
) -> schemas.ChatMessages:
    """
    get chat response
    """
    try:
        messages = (
            db.query(Message)
            .join(Chat)
            .filter(Chat.id == chat_id, Chat.user_id == user_id)
            .order_by(Message.created_at.desc())
            .all()
        )
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
            )

        return schemas.ChatMessages(
            messages=[
                schemas.Message(message=message.message, created_at=message.created_at)
                for message in messages
            ],
            user_id=user_id,
            chat_id=chat_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{traceback.format_exc()}",
        )


@router.post(
    "/chat",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ChatResponse,
)
def generate(
    chat_body: schemas.ChatBody,
    db: Session = Depends(deps.get_db),
) -> schemas.ChatResponse:
    """
    generates a chat response
    """

    try:
        if chat_body.chat_id is None:
            # create chat
            chat = Chat(user_id=chat_body.user_id)
            db.add(chat)
            db.commit()
            db.refresh(chat)
        else:
            chat = db.query(Chat).filter(Chat.id == chat_body.chat_id).first()
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
                )

        prev_messages = db.query(Message).filter(Message.chat_id == chat.id).all()

        # create a new message from body
        message = Message(chat_id=chat.id, message=chat_body.message, is_ai=False)
        db.add(message)
        db.commit()
        db.refresh(message)

        chat_bot = ChatBot()
        response = chat_bot.generate(query=message.message, messages=prev_messages)

        # save response to db
        msg_obj = Message(chat_id=chat.id, message=response, is_ai=True)
        db.add(msg_obj)
        db.commit()

        return schemas.ChatResponse(response=response, chat_id=chat.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{traceback.format_exc()}",
        )
