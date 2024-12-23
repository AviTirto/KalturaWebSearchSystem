FROM python:3.12-slim

# Install Firefox and required dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    xvfb \  # Add this for virtual framebuffer
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
    dbus \  # Add this for Firefox
    && rm -rf /var/lib/apt/lists/*

[... rest of Dockerfile remains the same ...]

# Add script to start Xvfb before the application
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Change the CMD to use the start script
CMD ["/start.sh"]