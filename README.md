```markdown
# MLOps Housing Price Prediction API - Milestone 2

![Build Status](https://github.com/kiranmusu14/ids568-mlops-project/actions/workflows/build.yml/badge.svg)

This repository contains a containerized FastAPI application that serves a machine learning model for housing price prediction. This milestone focuses on **containerization optimization**, **security**, and **automated CI/CD pipelines**.

## 🚀 Features
- **Multi-Stage Docker Build**: Optimized image size using a builder pattern to separate build-time dependencies from the runtime environment.
- **Security**: The application runs under a non-root `appuser` for enhanced container security.
- **Automated CI/CD**: Every push to `main` triggers automated unit testing and a push to Google Artifact Registry.
- **Unit Testing**: Verified test coverage for API endpoints and model inference using `pytest`.

---

## 🛠 Local Development

### 1. Setup Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt

```

### 2. Run Tests

```bash
pytest tests/test_app.py

```

### 3. Run with Docker

Build and run the container locally to verify the production environment:

```bash
docker build -t housing-api-v2 ./module3/milestone2
docker run -d -p 8080:8080 housing-api-v2

```

---

## ☁️ Registry Instructions

To pull and run the verified image directly from the Google Artifact Registry:

**Pull the image:**

```bash
docker pull us-central1-docker.pkg.dev/mlops-milestone1-486120/mlops-repo/housing-api-v2:latest

```

**Run the image:**

```bash
docker run -p 8080:8080 us-central1-docker.pkg.dev/mlops-milestone1-486120/mlops-repo/housing-api-v2:latest

```

---

## 🧪 API Verification

To test the prediction endpoint, send a POST request with the following 8 features:
`[MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]`

```bash
curl -X POST http://localhost:8080/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [3.5, 15.0, 5.0, 1.0, 800.0, 3.0, 34.0, -118.0]}'

```

**Expected Response:**

```json
{"prediction": 1.7518810030086698, "model_version": "1.0.0"}

```

---

## 🏗 CI/CD Architecture

The GitHub Actions workflow performs the following steps on every push:

1. **Lint & Test**: Runs `pytest` to ensure model and API logic are intact.
2. **GCP Auth**: Authenticates with Google Cloud via Service Account.
3. **Build & Push**: Builds the Docker image and pushes it to:
`us-central1-docker.pkg.dev/mlops-milestone1-486120/mlops-repo/housing-api-v2`.

---

## 📄 Documentation

For detailed information on the deployment strategy, security, and troubleshooting, please refer to the [RUNBOOK.md](https://www.google.com/search?q=./module3/milestone2/RUNBOOK.md).

```

---

### **Final Confirmation**
* **Repository Check**: All files are pushed to `module3/milestone2/`.
* **Tagging Check**: Your `m2-submission` tag is pushed and visible on GitHub.
* **Registry Check**: Your image is accessible in the course registry at `us-central1-docker.pkg.dev/mlops-milestone1-486120/mlops-repo/housing-api-v2`.

**You are 100% ready to submit!** Would you like me to help you double-check the specific file structure requirements for the submission portal one last time?

```