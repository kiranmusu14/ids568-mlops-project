from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Housing Price Prediction API is running"}

def test_prediction():
    # Adjust these keys to match your Milestone 1 input features
    test_data = {
        "MedInc": 3.5,
        "HouseAge": 15.0,
        "AveRooms": 5.0,
        "AveBedrms": 1.0,
        "Population": 800.0,
        "AveOccup": 3.0,
        "Latitude": 34.0,
        "Longitude": -118.0
    }
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    assert "prediction" in response.json()