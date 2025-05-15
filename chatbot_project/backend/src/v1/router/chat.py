from fastapi import APIRouter
from backend.src.v1.service.chat import run_llm
from backend.src.v1.model.model import ChatResponse,ChatRequest,SourceDocument
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from typing import List
from backend.src.v1.provider.history import  load_history, save_history
from fastapi import APIRouter, Depends, Header, HTTPException
from langchain.schema import HumanMessage, AIMessage,ChatMessage
router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_llm(
    req: ChatRequest,
    x_session_id: str = Header(...),            # giả sử frontend gởi header này
):
    # 1) Load history (List[ChatMessage])
    history_dto: List[ChatMessage] = load_history(x_session_id)

    # 2) Convert DTO -> BaseMessage để chạy LangChain
    history_msgs = []
    for m in history_dto:
        if m.role == "user":
            history_msgs.append(HumanMessage(content=m.content))
        else:
            history_msgs.append(AIMessage(content=m.content))

    # 3) Append user mới
    history_msgs.append(HumanMessage(content=req.query))

    # 4) Gọi LLM
    result, contexts = run_llm(req.query, history_msgs)

    # 5) Append AI trả về vào DTO
    history_dto.append(ChatMessage(role="user", content=req.query))
    history_dto.append(ChatMessage(role="assistant", content=result.answer))

    # 6) Save lại
    save_history(x_session_id, history_dto)

    # 7) Trả response
    return ChatResponse(
        answer=result.answer,
        contexts=[SourceDocument(source=d.metadata.get("source","")) for d in contexts],
        chat_history=history_dto
    )

# "contexts": [{"source": doc.metadata.get("source", "")} for doc in contexts],