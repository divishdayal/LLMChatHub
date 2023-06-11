from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class FetchedContent(BaseModel):
    url: str
    html: Optional[str]
    title: Optional[str]
    text: Optional[str]


class QAOuput(BaseModel):
    question: str
    answer: str
    sources: List


class ChatResponse(BaseModel):
    response: str


class Message(BaseModel):
    message: str
    created_at: datetime


class ChatMessages(BaseModel):
    user_id: int
    chat_id: int
    messages: List[Message]


class ChatBody(BaseModel):
    message: str
    user_id: int
    chat_id: Optional[int] = None


class UserCreate(BaseModel):
    email: str
    name: str
    username: str


class Response(BaseModel):
    message: str
