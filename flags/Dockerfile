FROM python:3.9-slim
WORKDIR /app

COPY flags/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY flags/app.py .
EXPOSE 5000

CMD ["python", "app.py"]