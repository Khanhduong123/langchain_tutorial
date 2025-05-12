from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from backend.src.v1.config.config import OPENAI_API_KEY,MODEL_EMBEDDING

def get_embedding_model() -> Embeddings:
    """
    Get the embedding model.
    """
    return OpenAIEmbeddings(model=MODEL_EMBEDDING,openai_api_key=OPENAI_API_KEY)