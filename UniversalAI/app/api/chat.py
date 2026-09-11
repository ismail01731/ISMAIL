from fastapi import APIRouter, Depends
from app.models.chat import ChatRequest
from app.brain.brain import process_message
from app.api.chat_history import add_message
from app.auth.dependencies import get_current_user
router = APIRouter()
@router.post("/chat")
async def chat(
    data: ChatRequest,
    current_user: str = Depends(get_current_user),
):
    chat_id = str(data.chat_id or "default")
    add_message(
        chat_id,
        "user",
        data.message,
        user_id=current_user,
    )
    result = await process_message(data.message)
    answer = result["answer"]
    add_message(
        chat_id,
        "assistant",
        answer,
        user_id=current_user,
    )
    return {
        "success": True,
        "chat_id": chat_id,
        "user_message": data.message,
        "intent": result["intent"],
        "plan": result["plan"],
        "reply": answer,
    }
