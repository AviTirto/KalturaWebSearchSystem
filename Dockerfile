# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY app /app

# Copy requirements.txt into the image
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV SRT_PATH="/app/links"
ENV LOCAL_DB_PATH="/app/db"

# Expose ports (FastAPI: 8000)
EXPOSE 8000

# Command to run FastAPI server
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port 8000"]
