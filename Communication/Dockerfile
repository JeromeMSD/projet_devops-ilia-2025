#Ce fichier a été réalisé par Mahdi HOBALLAH qui a recontré un problème d'accès à ce dépôt Github

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
# ============================
EXPOSE 8080

# ============================
# Application start command
# ============================
CMD ["python", "src/main.py"]

