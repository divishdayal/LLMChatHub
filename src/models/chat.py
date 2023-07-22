from sqlalchemy import BIGINT, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from src.db.base_class import Base

from .mixin import TimestampMixin


class Message(TimestampMixin, Base):
    __tablename__ = "messages"

    id = Column(BIGINT, primary_key=True, index=True, unique=True)
    message = Column(String, nullable=True)
    is_ai = Column(Boolean, default=False)

    chat_id = Column(BIGINT, ForeignKey("chats.id"), nullable=False)

    chat = relationship("Chat", back_populates="messages")


class Chat(TimestampMixin, Base):
    __tablename__ = "chats"

    id = Column(BIGINT, primary_key=True, index=True, unique=True)
    user_id = Column(BIGINT, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="chats")

    messages = relationship("Message", back_populates="chat", cascade="all")
