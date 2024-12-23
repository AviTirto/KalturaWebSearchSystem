FROM python:3.12-slim

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
    && rm -rf /var/lib/apt/lists/*

# Install newer SQLite3 from source
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450100.tar.gz \
    && tar xvfz sqlite-autoconf-3450100.tar.gz \
    && cd sqlite-autoconf-3450100 \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm -rf sqlite-autoconf-3450100 \
    && rm sqlite-autoconf-3450100.tar.gz

# Update dynamic linker run-time bindings
RUN ldconfig

# Set the working directory
WORKDIR /KalturaSearchSystem

# Copy the entire repository into the container first
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

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]