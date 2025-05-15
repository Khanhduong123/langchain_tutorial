import os
import tempfile,shutil
from fastapi import status
from pathlib import Path
from backend.src.v1.config.config import DATA_DIR
from backend.src.v1.service.ingest import ingest_text_documents_to_pinecone,ingest_pdf_documents_to_pinecone
from fastapi import APIRouter, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException

router = APIRouter(prefix="/documents", tags=["Documents"])
UPLOAD_DIR = Path(DATA_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF or TXT files are supported")
    else:
        if file.content_type == "application/pdf":
            os.makedirs(UPLOAD_DIR / "pdf", exist_ok=True)
            subfolder = "pdf"
        else:
            
            os.makedirs(UPLOAD_DIR / "txt", exist_ok=True)
            subfolder = "txt"

    file_path = UPLOAD_DIR /subfolder/file.filename

    try:
        with open(file_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to save file: {str(e)}")

    return {"filename": file.filename, "size": file_path.stat().st_size}

@router.get("/ingest")
async def ingest_all_uploaded_documents():
    txt_dir = UPLOAD_DIR / "txt"
    pdf_dir = UPLOAD_DIR / "pdf"

    txt_files = list(txt_dir.glob("*.txt")) if txt_dir.exists() else []
    pdf_files = list(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []

    if not txt_files and not pdf_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No PDF or TXT files found in upload directory.")

    for file_path in txt_files:
        ingest_text_documents_to_pinecone(str(file_path))

    for file_path in pdf_files:
        ingest_pdf_documents_to_pinecone(str(file_path))

    all_files = txt_files + pdf_files

    return {
        "status":status.HTTP_200_OK,
        "message": f"Ingested {len(all_files)} files into vector DB.",
        "files": [f.name for f in all_files]
    }


