# Use a lightweight Python image
FROM python:3.12-slim

# Install Firefox and Geckodriver dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    fontconfig \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libdbus-1-3 \
    libxt6 \
    libappindicator3-1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libgtk-3-0 \
    libgbm1 \
    firefox-esr

# Install Geckodriver (for Firefox WebDriver)
RUN FIREFOX_VERSION=$(firefox --version | awk '{print $3}') && \
    GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r .tag_name) && \
    curl -sL "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz" | tar xz -C /usr/local/bin

# Set the working directory to the root of the repository
WORKDIR /KalturaSearchSystem

# Copy requirements.txt into the image
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire repository into the container
COPY . .

# Set environment variables (adjust paths as needed)
ENV SRT_PATH="/KalturaSearchSystem/app/links"
ENV LOCAL_DB_PATH="/KalturaSearchSystem/app/db"

# Expose ports (FastAPI: 8000)
EXPOSE 8000

# Command to run FastAPI server
CMD ["sh", "-c", "uvicorn app.server:app --host 0.0.0.0 --port 8000"]
