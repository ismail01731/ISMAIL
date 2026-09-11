from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import json
import os
from datetime import datetime
from app.auth.dependencies import get_current_user
router = APIRouter()
HISTORY_FILE = "database/chat_history.json"
os.makedirs("database", exist_ok=True)
class HistoryRequest(BaseModel):
    chat_id: Optional[str] = None
    message: Optional[str] = None
    role: Optional[str] = None
    content: Optional[str] = None
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("History Load Error:", e)
        return {}
def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )
def add_message(chat_id, role, content, user_id="default"):
    history = load_history()
    user_id = str(user_id)
    chat_id = str(chat_id)
    if user_id not in history:
        history[user_id] = {}
    if chat_id not in history[user_id]:
        history[user_id][chat_id] = []
    history[user_id][chat_id].append(
        {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }
    )
    save_history(history)
@router.get("/chat/history")
async def get_history(
    chat_id: Optional[str] = None,
    current_user: str = Depends(get_current_user),
):
    history = load_history()
    user_history = history.get(
        str(current_user),
        {},
    )
    if chat_id is not None:
        return {
            "success": True,
            "chat_id": str(chat_id),
            "history": user_history.get(
                str(chat_id),
                [],
            ),
        }
    return {
        "success": True,
        "history": user_history,
    }
@router.post("/chat/history")
async def add_history(
    data: HistoryRequest,
    current_user: str = Depends(get_current_user),
):
    chat_id = str(data.chat_id or "default")
    content = data.content or data.message or ""
    role = data.role or "user"
    add_message(
        chat_id,
        role,
        content,
        user_id=current_user,
    )
    return {
        "success": True,
        "chat_id": chat_id,
        "message": {
            "role": role,
            "content": content,
        },
    }
