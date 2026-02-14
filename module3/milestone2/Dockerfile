# Stage 1: Build stage
FROM python:3.11-slim as builder
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final run stage
FROM python:3.11-slim
WORKDIR /app

# Security: Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local
# Copy app files
COPY app/ .

# Update PATH for the non-root user
ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser

EXPOSE 8080
CMD ["python", "main.py"]
