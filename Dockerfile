FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the necessary files first (for better caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend /app/backend
COPY firebase_key.json /app/firebase_key.json
COPY .env /app/.env

# Set environment variable for Python to prevent writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Set environment variable to ensure output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED 1

# Expose the FastAPI default port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
