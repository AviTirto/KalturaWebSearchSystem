# Use the official Python slim image
FROM python:3.12-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to match the actual path
WORKDIR /root/KalturaWebSearchSystem

# Create necessary directories
RUN mkdir -p /root/KalturaWebSearchSystem/db

# Copy everything except what's in .dockerignore
COPY . .

# Set environment variables to match the correct path
ENV DATABASE_PATH="/root/KalturaWebSearchSystem/database.db"
ENV LOCAL_DB_PATH="/root/KalturaWebSearchSystem/db"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure correct permissions for the database
RUN chmod -R 777 /root/KalturaWebSearchSystem/db
RUN chmod 777 /root/KalturaWebSearchSystem/database.db || true

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
