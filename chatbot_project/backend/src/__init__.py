from fastapi import APIRouter
from backend.src.v1.router.chat import router as chat_router
from backend.src.v1.router.documents import router as documents_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(chat_router)
api_v1_router.include_router(documents_router)