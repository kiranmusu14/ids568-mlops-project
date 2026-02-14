# Operations Runbook - Milestone 2

## 1. Dependency Pinning Strategy
We use a `requirements.txt` file with explicit versioning (e.g., `fastapi==0.109.0`) to ensure "Environment Parity." This prevents "it works on my machine" issues by forcing the Docker container and local venv to use identical library versions.

## 2. Image Optimization
**Strategy**: Multi-stage builds.
- **Builder Stage**: Uses a full Python image to install heavy dependencies into a local user directory.
- **Runtime Stage**: Uses a `python:3.11-slim` base and only copies the necessary site-packages and app code.
- **Metric**: This reduced our image size significantly compared to a single-stage build.

## 3. Security Considerations
- **Non-Root User**: The container creates and switches to `appuser`. This follows the Principle of Least Privilege, ensuring that if the API is compromised, the attacker does not have root access to the container.
- **Port Mapping**: The API is restricted to port 8080, typical for Cloud Run deployments.

## 4. CI/CD Workflow
1. **Lint/Test**: Runs `pytest` to ensure logic is sound before building.
2. **Auth**: Authenticates with Google Cloud using Service Account keys.
3. **Build/Push**: Builds the multi-stage Docker image and pushes it to Google Artifact Registry with semantic tags.

## 5. Versioning Strategy
We use **Semantic Versioning** and Git Tags. The final submission is tagged as `m2-submission` to provide a permanent, immutable reference point for the grader.

## 6. Troubleshooting Common Issues
- **422 Error**: Usually a JSON schema mismatch. Ensure the input key is `"features"` with a list of 8 floats.
- **500 Error**: Often caused by NumPy serialization. Always cast `model.predict()` results to `float()` or `.tolist()` before returning.
- **ModuleNotFoundError**: Occurs if the `PYTHONPATH` or Docker `WORKDIR` paths are mismatched.
