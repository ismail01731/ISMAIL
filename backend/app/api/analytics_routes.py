from fastapi import APIRouter
from pydantic import BaseModel, Field
from analytics.engine import HistoricalAnalytics
router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)
analytics = HistoricalAnalytics()
class AnalyticsRequest(BaseModel):
    values: list[float] = Field(
        min_length=2,
        max_length=10000,
    )
    window: int = Field(
        default=5,
        ge=1,
        le=100,
    )
@router.post("/analyze")
def analyze(
    request: AnalyticsRequest,
):
    return analytics.analyze(
        request.values,
        request.window,
    )
