from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from intelligence.orchestrator import FutureIntelligence
router = APIRouter(
    prefix="/api/intelligence",
    tags=["future-intelligence"],
)
intelligence = FutureIntelligence()
class IntelligenceRequest(BaseModel):
    question: str = Field(..., min_length=1)
    values: List[float] = Field(
        default_factory=list
    )
    evidence: Optional[List[Dict[str, Any]]] = None
    live_data: Optional[List[Dict[str, Any]]] = None
    horizon_days: int = Field(
        default=30,
        ge=1,
        le=3650,
    )
    metadata: Optional[Dict[str, Any]] = None
@router.post("/analyze")
def analyze(request: IntelligenceRequest):
    try:
        return intelligence.analyze(
            question=request.question,
            values=request.values,
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
