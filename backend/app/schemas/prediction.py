from pydantic import BaseModel, Field
class PredictionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=5000)
    horizon_days: int = Field(default=30, ge=1, le=3650)
    context: dict = Field(default_factory=dict)
class Scenario(BaseModel):
    name: str
    probability: float = Field(ge=0, le=1)
    explanation: str
class PredictionResponse(BaseModel):
    question: str
    horizon_days: int
    confidence: str
    scenarios: list[Scenario]
    disclaimer: str
