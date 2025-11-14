# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables for Python & Flask
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=src.main \
    FLASK_ENV=development \
    PORT=5010

# Install system dependencies
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port for Flask
EXPOSE 5010

# Run Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
