import functions_framework
import pickle
import numpy as np
import os

# Global variable for the model (allows "Warm Start" caching)
model = None

def load_model():
    """Loads the model from the local file if it hasn't been loaded yet."""
    global model
    if model is None:
        # The file is in the same directory as this script during execution
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)

@functions_framework.http
def predict_function(request):
    """
    HTTP Cloud Function entry point.
    """
    # 1. Handle CORS (Cross-Origin Resource Sharing) for browser testing
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {'Access-Control-Allow-Origin': '*'}

    # 2. Ensure model is loaded
    try:
        load_model()
    except Exception as e:
        return ({"error": f"Model loading failed: {str(e)}"}, 500, headers)

    # 3. Parse Request JSON
    request_json = request.get_json(silent=True)
    
    if request_json and 'features' in request_json:
        try:
            # 4. Predict
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