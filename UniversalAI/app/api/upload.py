from fastapi import APIRouter, UploadFile, File
import os
import shutil
from app.files.reader import read_pdf, read_docx
from app.files.chunker import chunk_text
from app.rag.retriever import save_document


router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extension = os.path.splitext(file.filename)[1].lower()

    text = ""

    if extension == ".pdf":
        text = read_pdf(file_path)

    elif extension == ".docx":
        text = read_docx(file_path)

    if text:

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):

            ok = save_document(
                f"{file.filename}_{index}",
                chunk
            )

            if not ok:
                print("Chunk Save Failed:", index)

    return {
        "success": True,
        "filename": file.filename,
        "path": file_path
    }