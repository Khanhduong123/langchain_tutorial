from typing import List, Dict
from backend.src.v1.model.model import ChatMessage

# Đây chỉ là ví dụ in‐memory. Thực tế dùng Redis/DB cho production.
_sessions: Dict[str, List[ChatMessage]] = {}

def load_history(session_id: str) -> List[ChatMessage]:
    return _sessions.get(session_id, [])

def save_history(session_id: str, history: List[ChatMessage]):
    _sessions[session_id] = history