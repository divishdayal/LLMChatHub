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
