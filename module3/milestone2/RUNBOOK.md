# Operations Runbook

## 1. Dependency Pinning Strategy
We use `requirements.txt` with strict version pinning (e.g., `fastapi==0.109.0`) to ensure reproducibility. This prevents unexpected updates from breaking the application in production.

## 2. Image Optimization
- **Before:** Standard build (~900MB)
- **After:** Multi-stage build (~200MB)
- **Technique:** We used a `builder` stage to compile dependencies and a `runtime` stage that only copies the necessary artifacts, discarding compilers and cache files.

## 3. Security Considerations
- **Non-Root User:** The container runs as user `1000`, limiting the potential impact if the container is compromised.
- **Minimal Base Image:** We use `python:3.11-slim` to reduce the attack surface.

## 4. CI/CD Workflow
1. **Push:** Developer pushes code to GitHub.
2. **Test:** GitHub Actions runs `pytest` to validate the model.
3. **Build:** If tests pass, Docker builds the image.
4. **Push:** The image is pushed to Google Artifact Registry.

## 5. Versioning Strategy
We use **Semantic Versioning** (e.g., `v1.0.0`). Git tags trigger specific deployments, ensuring we can roll back to previous versions if needed.

## 6. Troubleshooting
- **Tests Fail:** Check `tests/test_app.py` logs in GitHub Actions.
- **Auth Fail:** Verify `GCP_SA_KEY` in GitHub Secrets is valid and has "Artifact Registry Writer" permissions.
