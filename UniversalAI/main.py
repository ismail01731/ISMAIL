from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.upload import router as upload_router

app = FastAPI(
    title="Universal AI",
    version="1.0.0"
)

app.include_router(chat_router)
app.include_router(upload_router)

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Universal AI",
        "version": "1.0.0"
    }