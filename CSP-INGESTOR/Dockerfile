# ===========================================
# CSP-INGESTOR Dockerfile
# ===========================================

# 1️: Base image
FROM python:3.11-slim AS base

# 2️: Working directory inside the container
WORKDIR /app

# 3️: Copy only dependency file first (to leverage Docker layer caching)
COPY requirements.txt .

# 4️: Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5️: Copy the application code
COPY src/ ./src/
COPY swagger.yaml ./

# (Optional) Copy data files if needed during runtime
# COPY data/ ./data/

# 6️: Environment variables (customize if needed)
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
ENV SERVICE_NAME=CSP-INGESTOR

# 7️: Run your service (adjust if you use a framework)
CMD ["python", "src/main.py"]
