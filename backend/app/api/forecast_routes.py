from __future__ import annotations
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from forecast.engine import ForecastEngine
router = APIRouter(
    prefix="/api/forecast",
    tags=["forecast"],
)
engine = ForecastEngine()
class ForecastRequest(BaseModel):
    values: List[float] = Field(..., min_length=1)
    horizon_days: int = Field(default=30, ge=1, le=3650)
    evidence: Optional[List[Dict]] = None
@router.post("/predict")
def predict(request: ForecastRequest):
    try:
        return engine.predict(
            values=request.values,
            horizon_days=request.horizon_days,
            evidence=request.evidence,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
