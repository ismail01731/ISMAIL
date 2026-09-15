from __future__ import annotations
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pipeline.historical_ingest import HistoricalDataIngestor
router = APIRouter(
    prefix="/api/historical",
    tags=["historical"],
)
class HistoricalIngestRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    outputsize: str = "compact"
    limit: int | None = Field(
        default=None,
        ge=1,
        le=5000,
    )
@router.get("/status")
def historical_status() -> dict[str, Any]:
    ingestor = HistoricalDataIngestor()
    return {
        "status": "ready",
        "provider": "alphavantage",
        "api_key_configured": bool(
            ingestor.api_key
        ),
        "database": "sqlite",
    }
@router.post("/ingest")
def historical_ingest(
    request: HistoricalIngestRequest,
) -> dict[str, Any]:
    ingestor = HistoricalDataIngestor()
    if not ingestor.api_key:
        raise HTTPException(
            status_code=503,
            detail=(
                "ALPHA_VANTAGE_API_KEY "
                "is not configured"
            ),
        )
    try:
        return ingestor.ingest(
            symbol=request.symbol,
            outputsize=request.outputsize,
            limit=request.limit,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc
