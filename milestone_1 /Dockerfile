# 1. Use a lightweight Python base image
FROM python:3.9-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the application code and model
COPY . .

# 5. Define the command to run the app using the $PORT variable
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]