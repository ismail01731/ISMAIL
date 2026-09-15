from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    Scenario,
)
def predict(request: PredictionRequest) -> PredictionResponse:
    scenarios = [
        Scenario(
            name="Base case",
            probability=0.55,
            explanation="Current conditions continue without a major change.",
        ),
        Scenario(
            name="Positive change",
            probability=0.25,
            explanation="Conditions improve and the current trend becomes stronger.",
        ),
        Scenario(
            name="Negative change",
            probability=0.20,
            explanation="An unfavorable event changes the current trend.",
        ),
    ]
    return PredictionResponse(
        question=request.question,
        horizon_days=request.horizon_days,
        confidence="low",
        scenarios=scenarios,
        disclaimer=(
            "This system estimates possible outcomes probabilistically. "
            "It cannot know the future with certainty."
        ),
    )
