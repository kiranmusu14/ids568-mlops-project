import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import List

class PredictRequest(BaseModel):
    features: List[float]

    @field_validator('features') 
    @classmethod
    def validate_features_length(cls, v):
        if len(v) != 8:
            raise ValueError(f"Model expects exactly 8 features, but got {len(v)}")
        return v

class PredictResponse(BaseModel):
    prediction: float
    model_version: str

app = FastAPI()

# FIXED: Ensure path is relative to this specific script file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model = None

# Load model logic
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    else:
        # This will show up in your Docker/GitHub logs
        print(f"CRITICAL ERROR: model.pkl not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Housing Price Prediction API is running"}

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    if model is None:
        # Adding the path to the error message helps you debug in the browser/logs
        raise HTTPException(
            status_code=500, 
            detail=f"Model artifact not found at {MODEL_PATH}"
        )
    try:
        # Wrap features in a list for scikit-learn compatibility
        prediction = model.predict([data.features])[0]
        # Cast to float to ensure JSON serializability
        return PredictResponse(prediction=float(prediction), model_version="1.0.0")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")