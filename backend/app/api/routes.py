from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.predictor import predict
router = APIRouter()
@router.get("/health")
def health():
    return {"status": "healthy"}
@router.post("/predict", response_model=PredictionResponse)
def create_prediction(request: PredictionRequest):
    return predict(request)
