from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from live_data.manager import LiveDataManager
router = APIRouter(
    prefix="/live-data",
    tags=["Live Data"],
)
manager = LiveDataManager()
class LiveDataRequest(BaseModel):
    provider: str = Field(
        default="manual"
    )
    topic: str = Field(
        min_length=1,
        max_length=500,
    )
    value: object | None = None
    language: str = "en"
    sortBy: str = "publishedAt"
    pageSize: int = Field(
        default=10,
        ge=1,
        le=100,
    )
    function: str = "GLOBAL_QUOTE"
@router.get("/providers")
def providers():
    return {
        "providers":
            manager.available_providers()
    }
@router.post("/fetch")
def fetch_data(
    request: LiveDataRequest,
):
    try:
        items = manager.fetch(
            request.provider,
            request.topic,
            value=request.value,
            language=request.language,
            sortBy=request.sortBy,
            pageSize=request.pageSize,
            function=request.function,
        )
        return {
            "success": True,
            "provider": request.provider,
            "topic": request.topic,
            "count": len(items),
            "data": [
                item.to_dict()
                for item in items
            ],
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )
