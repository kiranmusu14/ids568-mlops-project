from fastapi.testclient import TestClient
import sys
import os

# Allow tests to find the 'app' folder
sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))

from main import app

client = TestClient(app)

def test_root():
    """Sanity check: Does the app start?"""
    response = client.get("/")
    # We accept 200 (OK) or 404 (Not Found) just to prove it didn't crash
    assert response.status_code in [200, 404]

def test_predict_valid():
    """Test: Do we get a prediction with valid data?"""
    payload = {
        "features": [8.3252, 41.0, 6.9841, 1.0238, 322.0, 2.5556, 37.88, -122.23]
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_invalid():
    """Test: Does it block bad data (Pydantic check)?"""
    payload = {"features": ["not", "numbers"]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
