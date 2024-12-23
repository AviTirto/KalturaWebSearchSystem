# Use the selenium standalone Firefox image as the base
FROM selenium/standalone-firefox:latest

# Set the working directory to the root of the repository
WORKDIR /KalturaSearchSystem

# Copy requirements.txt into the image
COPY requirements.txt .

# Install Python dependencies
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
