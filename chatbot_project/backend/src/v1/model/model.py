from pydantic import BaseModel
from typing import List, Dict, Any,Optional

class ChatMessage(BaseModel):
    message: str
    chat_history: List[Dict[str, Any]]

class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: List[str]
    raw_sources: List[str]

class DocumentUploadRequest(BaseModel):
    file_name: str
    description: Optional[str] = None