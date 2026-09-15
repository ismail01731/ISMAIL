from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
def test_predict():
    response = client.post(
        "/api/predict",
        json={
            "question": "What may happen in the next 30 days?",
            "horizon_days": 30
        },
    )
    assert response.status_code == 200
    assert len(response.json()["scenarios"]) == 3
