from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List
from forecast.backtesting import BacktestingEngine
router = APIRouter(
    prefix="/api/forecast",
    tags=["Forecast Backtesting"],
)
class BacktestRequest(BaseModel):
    values: List[float] = Field(
        ...,
        min_length=5,
    )
    validation_size: int = Field(
        default=3,
        ge=1,
        le=30,
    )
@router.post("/backtest")
def backtest(request: BacktestRequest):
    engine = BacktestingEngine()
    return engine.evaluate(
        values=request.values,
        validation_size=request.validation_size,
    )
