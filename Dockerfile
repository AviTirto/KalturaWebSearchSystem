FROM python:3.12-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /root/KalturaWebSearchSystem

# Create necessary directories
RUN mkdir -p /root/KalturaSearchSystem/db

# Copy everything except what's in .dockerignore
COPY . .

# Set environment variables to match your local paths
ENV DATABASE_PATH="/KalturaSearchSystem/database.db"
ENV LOCAL_DB_PATH="/KalturaSearchSystem/db"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure correct permissions for database directories
RUN chmod -R 777 /root/KalturaSearchSystem/db
RUN chmod 777 /KalturaSearchSystem/database.db || true

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]