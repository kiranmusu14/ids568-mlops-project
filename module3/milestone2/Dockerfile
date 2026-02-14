# STAGE 1: Builder (The "Kitchen")
# We use this stage to compile dependencies
FROM python:3.11-slim as builder

WORKDIR /build

# Copy requirements file
COPY app/requirements.txt .

# Install dependencies into a local directory (--user)
# This makes it easier to copy them to the next stage
RUN pip install --user --no-cache-dir -r requirements.txt

# STAGE 2: Runtime (The "Dining Room")
# We use a fresh image and only copy what we need
FROM python:3.11-slim as runtime

# Create a non-root user for security (Rubric requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy the installed libraries from the builder stage
COPY --from=builder /root/.local /home/user/.local

# Copy the application code
COPY --chown=user:user app/ .

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
