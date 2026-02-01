```markdown
# IDS 568 MLOps - Milestone 1: Housing Price Prediction API

**Author:** Kiran Kumar Srinivasa
**Course:** IDS 568 - MLOps (University of Illinois Chicago)

This project implements a Machine Learning API for predicting housing prices using **FastAPI** (Containerized) and **Google Cloud Functions** (Serverless). It demonstrates two different deployment strategies for the same ML model.

## 🚀 Live Deployments

| Component | Type | URL |
| :--- | :--- | :--- |
| **Cloud Run** | Container (FastAPI) | `https://mlops-api-385501609124.us-central1.run.app` |
| **Cloud Function** | Serverless (Gen 2) | `https://us-central1-mlops-milestone1-486120.cloudfunctions.net/mlops-function` |

## 📂 Project Structure
```text
ids568-mlops-project/
├── milestone_1/
│   ├── main.py              # FastAPI app (Cloud Run entry point)
│   ├── function_deploy/     # Deployment folder for Cloud Function
│   │   └── main.py          # Cloud Function entry point
│   ├── train_model.py       # Script to train/save model.pkl
│   ├── model.pkl            # Serialized model artifact
│   ├── requirements.txt     # Dependencies
│   └── Dockerfile           # Container config
└── README.md                # Documentation & Comparative Report

```

## 🛠️ Setup & Installation

**1. Environment Setup**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r milestone_1/requirements.txt

```

**2. Local Testing (FastAPI)**

```bash
cd milestone_1
uvicorn main:app --reload
# Test at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

```

---

## ☁️ Deployment Guide

### Strategy A: Cloud Run (Container)

The primary deployment uses a Docker container running FastAPI.

1. **Build & Push Image:**
```bash
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
# Deployed from 'function_deploy' folder containing main.py and model.pkl
gcloud functions deploy mlops-function \
    --gen2 --runtime=python311 --source=. --entry-point=predict_function \
    --trigger-http --allow-unauthenticated

```



---

## 📘 Lifecycle & Artifact Management (Rubric Requirement)

### 1. Deployment Stage Explanation

* **Cloud Run (Container):** The application runs as a long-lived service. The `model.pkl` is loaded into memory **once** during the container startup sequence (managed by FastAPI's lifespan events). This allows the service to handle high concurrency with low latency after the initial boot.
* **Cloud Function (Serverless):** The function is ephemeral. The model is loaded lazily via a global variable check. Google's infrastructure manages the environment; if the function is triggered frequently, the environment stays "warm" (keeping the model in memory). If idle, it shuts down completely.

### 2. Model-API Interaction

Data flow ensures strict validation:

1. **Input:** Client sends `{"features": [8.32, 41.0, ...]}` (JSON).
2. **Validation:** Pydantic schemas enforce that the input is a list of exactly 8 floats.
3. **Inference:** Data is converted to a NumPy array `(1, -1)` for the Scikit-Learn model.
4. **Output:** Prediction is returned as JSON with model version metadata.

---

## 📊 Comparative Report: Cloud Run vs. Cloud Function

| Metric | Cloud Run (Container) | Cloud Function (Serverless) |
| --- | --- | --- |
| **Latency (Cold Start)** | **High (~3-5s):** Must boot full OS/Container. | **Medium (~1-2s):** Lighter weight environment. |
| **Latency (Warm)** | **Lowest:** High-performance asyncio server (Uvicorn). | **Low:** Minimal overhead, but slightly slower than pure FastAPI. |
| **Artifact Loading** | Deterministic (at startup). Fails fast if model is missing. | Lazy (on first request). Easier to deploy updates. |
| **State** | Stateless service, but keeps memory cache active. | Strictly stateless execution. |
| **Reproducibility** | **Perfect:** `Dockerfile` freezes OS & deps. | **Good:** Relies on `requirements.txt` & Google Runtime. |

---

## 🧪 Testing

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