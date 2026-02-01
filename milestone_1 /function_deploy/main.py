import functions_framework
import joblib  # <--- Switched from pickle to joblib
import numpy as np
import os

# Global variable for the model
model = None

def load_model():
    """Loads the model using joblib (better for sklearn models)."""
    global model
    if model is None:
        # Load directly using joblib
        model = joblib.load('model.pkl')

@functions_framework.http
def predict_function(request):
    """HTTP Cloud Function entry point."""
    
    # 1. Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    # 2. Ensure model is loaded
    try:
        load_model()
    except Exception as e:
        return ({"error": f"Model loading failed: {str(e)}"}, 500, headers)

    # 3. Parse Request
    request_json = request.get_json(silent=True)
    
    if request_json and 'features' in request_json:
        try:
            features = np.array(request_json['features']).reshape(1, -1)
            prediction = model.predict(features)[0]
            
            response = {
                "prediction": prediction,
                "model_version": "1.0.0",
                "backend": "Google Cloud Function"
            }
            return (response, 200, headers)
        except Exception as e:
            return ({"error": str(e)}, 400, headers)
            
    return ({"error": "JSON body must include 'features' list"}, 400, headers)