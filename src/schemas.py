from typing import Any, Dict, List, Optional

from pydantic import BaseModel

class FetchedContent(BaseModel):
    url: str
    html: Optional[str]
    title: Optional[str]
    text: Optional[str]

class QAOuput(BaseModel):
    """Output data model for API. It follows the format that is expected from Vertex AI."""
    question: str
    answer: str
    sources: List