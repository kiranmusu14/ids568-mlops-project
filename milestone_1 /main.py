import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator # Updated import
from typing import List

class PredictRequest(BaseModel):
    features: List[float]

    # NEW: Pydantic V2 syntax
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

MODEL_PATH = "model.pkl"
model = None

# Load model logic
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {os.getcwd()}")
else:
    print(f"Warning: model.pkl not found in {os.getcwd()}. API will return errors.")

@app.get("/")
def read_root():
    return {"message": "Housing Price Prediction API is running"}

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model artifact not found")
    try:
        prediction = model.predict([data.features])[0]
        return PredictResponse(prediction=float(prediction), model_version="1.0.0")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))