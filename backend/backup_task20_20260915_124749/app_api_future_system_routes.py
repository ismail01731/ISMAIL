from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from future_system.system import CompleteFutureSystem
router = APIRouter(
    prefix="/api/future",
    tags=["complete-future-intelligence"],
)
system = CompleteFutureSystem()
class FutureRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
    )
    historical_values: List[float] = Field(
        default_factory=list
    )
    evidence: Optional[
        List[Dict[str, Any]]
    ] = None
    live_data: Optional[
        List[Dict[str, Any]]
    ] = None
    horizon_days: int = Field(
        default=30,
        ge=1,
        le=3650,
    )
    metadata: Optional[
        Dict[str, Any]
    ] = None
@router.post("/analyze")
def complete_future_analysis(
    request: FutureRequest,
):
    try:
        return system.analyze(
            question=request.question,
            historical_values=
                request.historical_values,
            evidence=request.evidence,
            live_data=request.live_data,
            horizon_days=request.horizon_days,
            metadata=request.metadata,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
@router.get("/status")
def future_system_status():
    return {
        "system":
            "ISMAIL Future Intelligence System",
        "version":
            "1.0.0",
        "status":
            "ready",
        "components": {
            "prediction_core":
                "ready",
            "evidence_intelligence":
                "ready",
            "live_data":
                "ready",
            "historical_database":
                "ready",
            "historical_analytics":
                "ready",
            "forecast_engine":
                "ready",
            "existing_ai_adapter":
                (
                    "connected"
                    if system.ai_adapter.connected
                    else "waiting_for_existing_ai"
                ),
            "feedback_tracking":
                "ready",
        },
    }
