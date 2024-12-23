# Use a more standard base image that's known to work well on Render
FROM python:3.9-slim-buster

# Install Firefox and required dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.33.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.33.0-linux64.tar.gz

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libgdk-pixbuf2.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    curl \
    jq \
    fontconfig \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /KalturaSearchSystem

# Copy requirements.txt into the image
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire repository into the container
COPY . .

# Set environment variables
ENV SRT_PATH="/KalturaSearchSystem/app/links"
ENV LOCAL_DB_PATH="/KalturaSearchSystem/app/db"

# Create necessary directories
RUN mkdir -p ${SRT_PATH} ${LOCAL_DB_PATH}

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]