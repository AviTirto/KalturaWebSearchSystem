# Use the official Python 3.12-slim image as a base
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
WORKDIR /KalturaSearchSystem

# Copy the entire repository into the container
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH="/KalturaSearchSystem:${PYTHONPATH}"

# Set environment variables for the database
# Point to a directory inside the container
ENV DATABASE_PATH="/KalturaSearchSystem/db/database.db"
# If you want to change the default directory from `./db`, modify this line in the code:
ENV LOCAL_DB_PATH="/KalturaSearchSystem/db"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
