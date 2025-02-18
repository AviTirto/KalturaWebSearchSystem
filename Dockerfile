# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code and config files
COPY backend /app/backend

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update paths to point to the new config file locations
ENV FIREBASE_KEY_PATH=/app/backend/firebase_key.json
ENV ENV_FILE=/app/backend/.env

EXPOSE 8000

CMD ["uvicorn", "backend.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
