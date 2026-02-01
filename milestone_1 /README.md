```markdown
# IDS 568 MLOps - Milestone 1: Housing Price Prediction API

Author: Kiran Kumar Srinivasa
Course: IDS 568 - MLOps 

This project implements a Machine Learning API for predicting housing prices using FastAPI (Containerized) and Google Cloud Functions (Serverless). It demonstrates two different deployment strategies for the same ML model.

# Live Deployments

| Component | Type | URL |
| :--- | :--- | :--- |
| Cloud Run | Container (FastAPI) | `https://mlops-api-385501609124.us-central1.run.app` |
| Cloud Function | Serverless (Gen 2) | `https://us-central1-mlops-milestone1-486120.cloudfunctions.net/mlops-function` |

# Project Structure & Artifacts

The project is organized into the following key files. (Note: All source code is located in the `milestone_1` directory.)

| File | Description |
| :--- | :--- |
| `milestone_1/main.py` | **Cloud Run Entry Point:** The main FastAPI application. Defines the `/predict` endpoint and handles Pydantic schema validation. |
| `milestone_1/function_deploy/main.py` | **Cloud Function Entry Point:** The adapted Python script for the Serverless deployment. Uses `joblib` for lazy model loading. |
| `milestone_1/model.pkl` | **Model Artifact:** The serialized Scikit-Learn regression model. Loaded by both the API and the Function to make predictions. |
| `milestone_1/train_model.py` | **Training Script:** The Python script used to train the model on the California Housing dataset and save it as `model.pkl`. |
| `milestone_1/Dockerfile` | **Container Config:** Instructions for Docker to build the Linux environment, install dependencies, and launch `uvicorn`. |
| `milestone_1/requirements.txt`| **Dependencies:** Lists all required Python libraries (FastAPI, Scikit-Learn, Joblib, etc.) to ensure a reproducible environment. |

##  Setup & Installation

**IMPORTANT:** You must navigate into the `milestone_1` folder before running any of the commands below.

**1. Clone & Environment Setup**
```bash
# Clone the repository
git clone [https://github.com/kiranmusu14/ids568-mlops-project.git](https://github.com/kiranmusu14/ids568-mlops-project.git)
cd ids568-mlops-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r milestone_1/requirements.txt

```

**2. Local Testing (FastAPI)**

```bash
# Navigate to the source folder
cd milestone_1

# Run the server
uvicorn main:app --reload
# Access documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

```

---

## Deployment Guide

### Strategy A: Cloud Run (Container)

The primary deployment uses a Docker container running FastAPI.

1. **Build & Push Image:**
```bash
cd milestone_1  # Ensure you are in the correct folder

# Note: --platform linux/amd64 is required for Mac M1/M2 chips
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/mlops-milestone1-486120/mlops-repo/fastapi-service:v1 .
docker push us-central1-docker.pkg.dev/mlops-milestone1-486120/mlops-repo/fastapi-service:v1

```


2. **Deploy Service:**
```bash
gcloud run deploy mlops-api \
    --image=us-central1-docker.pkg.dev/mlops-milestone1-486120/mlops-repo/fastapi-service:v1 \
    --allow-unauthenticated

```



### Strategy B: Cloud Function (Serverless)

A lightweight function for on-demand inference.

1. **Prepare & Deploy:**
```bash
cd milestone_1  # Ensure you are in the correct folder

# Deployed from 'function_deploy' folder containing main.py and model.pkl
gcloud functions deploy mlops-function \
    --gen2 --runtime=python311 --source=function_deploy --entry-point=predict_function \
    --trigger-http --allow-unauthenticated

```



---

## Lifecycle & Artifact Management (Rubric Requirement)

### 1. Deployment Stage Explanation

* **Cloud Run (Container):** The application runs as a long-lived service. The `model.pkl` is loaded into memory **once** during the container startup sequence (managed by FastAPI's lifespan events). This allows the service to handle high concurrency with low latency after the initial boot.
* **Cloud Function (Serverless):** The function is ephemeral. The model is loaded lazily via a global variable check using `joblib`. Google's infrastructure manages the environment; if the function is triggered frequently, the environment stays "warm" (keeping the model in memory). If idle, it shuts down completely.

### 2. Model-API Interaction

Data flow ensures strict validation:

1. **Input:** Client sends `{"features": [8.32, 41.0, ...]}` (JSON).
2. **Validation:** Pydantic schemas enforce that the input is a list of exactly 8 floats.
3. **Inference:** Data is converted to a NumPy array `(1, -1)` for the Scikit-Learn model.
4. **Output:** Prediction is returned as JSON with model version metadata.

---

## Comparative Report: Cloud Run vs. Cloud Function

| Metric | Cloud Run (Container) | Cloud Function (Serverless) |
| --- | --- | --- |
| **Latency (Cold Start)** | **High (~3-5s):** Must boot full OS/Container. | **Medium (~1-2s):** Lighter weight environment. |
| **Latency (Warm)** | **Lowest:** High-performance asyncio server (Uvicorn). | **Low:** Minimal overhead, but slightly slower than pure FastAPI. |
| **Artifact Loading** | Deterministic (at startup). Fails fast if model is missing. | Lazy (on first request). Easier to deploy updates. |
| **State** | Stateless service, but keeps memory cache active. | Strictly stateless execution. |
| **Reproducibility** | **Perfect:** `Dockerfile` freezes OS & deps. | **Good:** Relies on `requirements.txt` & Google Runtime. |

---

## Testing

**Test Cloud Run:**

```bash
curl -X POST "[https://mlops-api-385501609124.us-central1.run.app/predict](https://mlops-api-385501609124.us-central1.run.app/predict)" \
     -H "Content-Type: application/json" \
     -d '{"features": [8.3252, 41.0, 6.9841, 1.0238, 322.0, 2.5556, 37.88, -122.23]}'

```

**Test Cloud Function:**

```bash
curl -X POST "[https://us-central1-mlops-milestone1-486120.cloudfunctions.net/mlops-function](https://us-central1-mlops-milestone1-486120.cloudfunctions.net/mlops-function)" \
     -H "Content-Type: application/json" \
     -d '{"features": [8.3252, 41.0, 6.9841, 1.0238, 322.0, 2.5556, 37.88, -122.23]}'

```

```

```