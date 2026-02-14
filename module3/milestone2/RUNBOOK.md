# Milestone 2 Runbook

## Project Overview
This project automates the deployment of a Housing Price Prediction API using a CI/CD pipeline.

## Docker Optimization
- **Multi-stage build**: Uses a `builder` stage to install dependencies and a final stage for execution to minimize image size.
- **Security**: The container runs as a non-root `appuser`.

## CI/CD Pipeline
- **Trigger**: The pipeline runs on every push of a version tag (e.g., `v1.0.4`).
- **Steps**:
  1. **Test**: Runs `pytest` to verify API functionality.
  2. **Auth**: Authenticates with Google Cloud using GitHub Secrets.
  3. **Build & Push**: Builds the Docker image and pushes it to Google Artifact Registry.

## Deployment Commands
To deploy a new version:
1. `git tag v1.0.x`
2. `git push origin v1.0.x`