from __future__ import annotations
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field
from feedback.engine import FeedbackEngine
router = APIRouter(
    prefix="/api/feedback",
    tags=["feedback"],
)
engine = FeedbackEngine()
class FeedbackRequest(BaseModel):
    prediction_id: int = Field(
        default=0,
        ge=0,
    )
    predicted_value: float
    actual_value: float
    confidence: float = Field(
        default=0.5,
        ge=0,
        le=1,
    )
    notes: Optional[str] = None
@router.post("/record")
def record_feedback(
    request: FeedbackRequest,
):
    return engine.record(
        prediction_id=request.prediction_id,
        predicted_value=request.predicted_value,
        actual_value=request.actual_value,
        confidence=request.confidence,
        notes=request.notes,
    )
@router.get("/summary")
def feedback_summary():
    return engine.summary()
@router.get("/history")
def feedback_history():
    return {
        "items":
            engine.storage.list_all()
    }
