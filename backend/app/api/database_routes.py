from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from database.connection import Database
from database.models import HistoricalRecord
from database.repositories.historical import HistoricalRepository
router = APIRouter(
    prefix="/database",
    tags=["Database"],
)
repository = HistoricalRepository(
    Database()
)
class HistoricalDataRequest(BaseModel):
    topic: str = Field(
        min_length=1,
        max_length=500,
    )
    value: str
    source: str = ""
    source_type: str = "unknown"
    timestamp: str
    reliability: float = Field(
        default=0.50,
        ge=0.0,
        le=1.0,
    )
    metadata: dict = Field(
        default_factory=dict
    )
@router.get("/status")
def database_status():
    return {
        "status": "online",
        "historical_records":
            repository.count(),
    }
@router.post("/historical")
def save_historical_data(
    request: HistoricalDataRequest,
):
    record = HistoricalRecord(
        topic=request.topic,
        value=request.value,
        source=request.source,
        source_type=request.source_type,
        timestamp=request.timestamp,
        reliability=request.reliability,
        metadata=request.metadata,
    )
    record_id = repository.insert(
        record
    )
    return {
        "success": True,
        "id": record_id,
    }
@router.get("/historical/{topic}")
def get_historical_data(
    topic: str,
    limit: int = 100,
):
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )
    return {
        "topic": topic,
        "count": repository.count(
            topic
        ),
        "data": repository.list_by_topic(
            topic,
            limit,
        ),
    }
