FROM python:3.12-slim

# Install Firefox and required dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    xvfb \
    dbus-x11 \  # Add this
    && rm -rf /var/lib/apt/lists/*

# Install geckodriver with the correct version (0.35.0)
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.35.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.35.0-linux64.tar.gz

# Install system dependencies and newer SQLite3
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
    sqlite3 \
    dbus \
    && rm -rf /var/lib/apt/lists/*

# Update dynamic linker run-time bindings
RUN ldconfig

# Set the working directory
WORKDIR /KalturaSearchSystem

# Copy the entire repository into the container
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH="/KalturaSearchSystem:${PYTHONPATH}"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV SRT_PATH="/KalturaSearchSystem/app/links"
ENV LOCAL_DB_PATH="/KalturaSearchSystem/app/db"

# Create necessary directories
RUN mkdir -p ${SRT_PATH} ${LOCAL_DB_PATH}

# Add display environment variable for Firefox
ENV DISPLAY=:99

# Add script to start Xvfb before the application
COPY start.sh /start.shx
RUN chmod +x /start.sh

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI server using the start script
CMD ["/start.sh"]