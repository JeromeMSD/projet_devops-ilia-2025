
FROM python:3.12-slim AS base


RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ ./src

# ============================
# Expose API port
# Change 8000 if needed
# ============================
EXPOSE 8000

# ============================
# Application start command
# If using FastAPI: replace CMD line
# ============================
CMD ["python", "src/main.py"]
