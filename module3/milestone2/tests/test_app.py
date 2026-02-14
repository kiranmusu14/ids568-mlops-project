from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """Verifies that the root endpoint is alive."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Housing Price Prediction API is running"}

def test_prediction():
    """Verifies the /predict endpoint with the validated input format."""
    test_data = {
        "features": [3.5, 15.0, 5.0, 1.0, 800.0, 3.0, 34.0, -118.0]
    }
    
    response = client.post("/predict", json=test_data)
    
    # This now passes because the 500 error is fixed!
    assert response.status_code == 200
    
    data = response.json()
    assert "prediction" in data
    
    # FIXED: Check for float instead of list to match your main.py logic
    assert isinstance(data["prediction"], float)
    assert "model_version" in data