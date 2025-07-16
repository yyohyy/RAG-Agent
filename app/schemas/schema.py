from pydantic import BaseModel, Field
from typing import Optional

class ChatIn(BaseModel):
    question: str = Field()
    session_id: Optional[str] = None
