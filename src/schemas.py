from typing import Any, Dict, List, Optional

from pydantic import BaseModel

class FetchedContent(BaseModel):
    url: str
    html: Optional[str]
    title: Optional[str]
    text: Optional[str]
