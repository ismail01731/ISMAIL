from pydantic import BaseModel
from typing import Optional, Any
class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None
    user_id: Optional[str] = None
    file_context: Optional[Any] = None
