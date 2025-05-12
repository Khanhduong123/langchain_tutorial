from langchain_openai import ChatOpenAI
from backend.src.v1.config.config import OPENAI_API_KEY,MODEL_CHAT

def get_chat_model() -> ChatOpenAI:
    """
    Get the chat model.
    """
    return ChatOpenAI(model=MODEL_CHAT, temperature=0, openai_api_key=OPENAI_API_KEY)