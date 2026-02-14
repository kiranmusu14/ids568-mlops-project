# Stage 1: Build stage
FROM python:3.11-slim AS builder
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final run stage
FROM python:3.11-slim

# Security: Create a non-root user BEFORE setting WORKDIR
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory and change ownership
WORKDIR /app
RUN chown -R appuser:appuser /app

# Copy installed dependencies from builder with correct ownership
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy app files with correct ownership
COPY --chown=appuser:appuser app/ .

# Update PATH for the non-root user
ENV PATH=/home/appuser/.local/bin:$PATH

# Switch to non-root user
USER appuser

EXPOSE 8080

# Health check (optional but recommended)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# We remove 'app.' because the files were copied directly to the WORKDIR
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]