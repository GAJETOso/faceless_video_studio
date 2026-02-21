# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies for MoviePy, ImageMagick, and Audio processing
RUN apt-get update && apt-get install -y \
    imagemagick \
    ffmpeg \
    libmagic1 \
    fonts-liberation \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick security policy to allow text-to-video processing
RUN find /etc -name "policy.xml" -exec sed -i 's/domain="path" rights="none" pattern="@\*"/domain="path" rights="read|write" pattern="@\*"/g' {} +

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create necessary directories for assets and output
RUN mkdir -p assets output scripts

# Set environment variables (Placeholders - should be set in Cloud Provider)
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Start the API server
CMD ["python", "api.py"]
