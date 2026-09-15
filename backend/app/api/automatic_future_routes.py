from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pipeline.automatic import AutomaticFuturePipeline
router = APIRouter(
    prefix="/api/future",
    tags=["automatic-future"],
)
class AutomaticFutureRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
    )
    topic: str = Field(
        ...,
        min_length=1,
    )
    horizon_days: int = Field(
        default=30,
        ge=1,
        le=3650,
    )
    live_provider: Optional[str] = None
    live_value: Optional[Any] = None
    historical_limit: int = Field(
        default=200,
        ge=1,
        le=5000,
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )
_pipeline = AutomaticFuturePipeline()
@router.post("/automatic")
def automatic_future(
    request: AutomaticFutureRequest,
):
    try:
        return _pipeline.analyze(
            question=request.question,
            topic=request.topic,
            horizon_days=request.horizon_days,
            live_provider=request.live_provider,
            live_value=request.live_value,
            historical_limit=request.historical_limit,
            metadata=request.metadata,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
@router.get("/automatic/status")
def automatic_future_status():
    return {
        "status": "ok",
        "pipeline": "automatic_future",
        "historical_source": "sqlite",
        "live_data_supported": True,
        "existing_ai_preserved": True,
        "new_ai_created": False,
    }
