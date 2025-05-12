from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.src.v1.service.chat import run_llm


router = APIRouter(prefix="/chat", tags=["Chat"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            await run_llm(data, websocket)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})