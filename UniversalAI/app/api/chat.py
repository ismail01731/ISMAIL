from fastapi import APIRouter
from app.models.chat import ChatRequest
from app.brain.brain import process_message

router = APIRouter()


@router.post("/chat")
async def chat(data: ChatRequest):

    result = await process_message(data.message)

    return {
        "success": True,
        "user_message": data.message,
        "intent": result["intent"],
        "plan": result["plan"],
        "reply": result["answer"]
    }