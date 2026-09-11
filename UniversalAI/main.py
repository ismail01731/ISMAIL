from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat_history import router as chat_history_router

from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.auth.router import router as auth_router


app = FastAPI(
    title="Universal AI",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# API ROUTES
# =========================================================

app.include_router(
    chat_router,
    prefix="/api"
)

app.include_router(
    chat_history_router,
    prefix="/api"
)

app.include_router(
    upload_router,
    prefix="/api/file"
)

app.include_router(
    auth_router,
    prefix="/api/auth"
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
async def home():
    return {
        "status": "running",
        "project": "Universal AI",
        "version": "1.0.0"
    }