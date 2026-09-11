from fastapi import APIRouter, UploadFile, File, Depends
import os
import shutil
from app.files.reader import read_pdf, read_docx
from app.files.chunker import chunk_text
from app.rag.retriever import save_document
from app.auth.dependencies import get_current_user
router = APIRouter()
UPLOAD_FOLDER = "uploads"
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True,
)
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
):
    safe_filename = os.path.basename(
        file.filename
    )
    file_path = os.path.join(
        UPLOAD_FOLDER,
        safe_filename,
    )
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )
    extension = os.path.splitext(
        safe_filename
    )[1].lower()
    text = ""
    if extension == ".pdf":
        text = read_pdf(file_path)
    elif extension == ".docx":
        text = read_docx(file_path)
    if text:
        chunks = chunk_text(text)
        for index, chunk in enumerate(chunks):
            doc_id = (
                f"{current_user}_"
                f"{safe_filename}_"
                f"{index}"
            )
            ok = save_document(
                doc_id,
                chunk,
            )
            if not ok:
                print(
                    "Chunk Save Failed:",
                    index,
                )
    return {
        "success": True,
        "filename": safe_filename,
        "path": file_path,
        "user_id": current_user,
    }
