# ids568-mlops-project
# MLOps Project: Environment & CI Setup
[![CI Pipeline](https://github.com/kiranmusu14/ids568-mlops-project/actions/workflows/ci.yml/badge.svg)](https://github.com/kiranmusu14/ids568-mlops-project/actions/workflows/ci.yml)

## 📌 Project Overview
This repository serves as the foundational infrastructure for an end-to-end MLOps pipeline. It establishes a **deterministic, reproducible Python environment** designed to eliminate "training-serving skew" and ensure reliability across the machine learning lifecycle.

This work fulfills **Milestone 0** for the MLOps course, demonstrating the integration of version control, strict dependency management, and Continuous Integration (CI) automation.

---

## 📂 Project Structure
```text
ids568-mlops-project/
├── .github/workflows/
│   └── ci.yml            # CI pipeline configuration (GitHub Actions)
├── tests/
│   └── test_smoke.py     # Smoke tests for environment validation
├── requirements.txt      # Pinned production dependencies (Exact versions)
├── README.md             # Project documentation and CI status
└── .gitignore            # Git exclusion rules

## Reproducibility & The ML Lifecycle
**1. Why Environment Reproducibility Matters (CG1.LO1):**
In the ML lifecycle, moving from experimentation to production is often the point of failure. A model trained in one environment (e.g., specific versions of NumPy or Scikit-Learn) may fail silently or error out in another. By strictly pinning dependencies in `requirements.txt`, this project ensures that the computation environment is deterministic. This "contract" guarantees that anyone—or any machine—can replicate the exact conditions under which the code was developed, preventing the common "it works on my machine" anti-pattern.

**2. Principles Applied (CG1.LO2):**
* **Dependency Pinning:** All libraries are locked to specific versions (e.g., `pandas==2.2.0`) rather than open ranges.
* **Isolation:** The project uses a virtual environment (`venv`) to avoid conflicts with system-level packages.
* **Automated Validation:** A "smoke test" (`test_smoke.py`) runs automatically via GitHub Actions to verify that the environment builds correctly and imports succeed.

**3. Connection to Deployment (CG1.LO3):**
The CI pipeline acts as a safety gate. Before any code is merged or deployed, the system proves that the environment can be recreated from scratch on a clean machine (Ubuntu runner). This foundational step is critical for scalable MLOps, ensuring that data pipelines and model artifacts rely on a stable, verified infrastructure.