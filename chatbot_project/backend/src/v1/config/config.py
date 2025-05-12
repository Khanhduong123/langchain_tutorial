import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY",'Not Provided')
INDEX_NAME = os.getenv("INDEX_NAME",'Not Provided')
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", 'Not Provided')
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING")
MODEL_CHAT = os.getenv("MODEL_CHAT")
DATA_DIR = "backend/src/v1/data"