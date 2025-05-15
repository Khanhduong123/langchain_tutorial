from pydantic import BaseModel
from typing import List, Dict, Any,Optional
from langchain.schema.messages import BaseMessage
class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    query: str
    
class SourceDocument(BaseModel):
    source: str

class ChatResponse(BaseModel):
    answer: str
    contexts: List[SourceDocument] = []
    chat_history:  List[BaseMessage] = [] 

class DocumentUploadRequest(BaseModel):
    file_name: str
    description: Optional[str] = None