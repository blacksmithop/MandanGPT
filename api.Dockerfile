FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir fastapi uvicorn jinja2 itsdangerous httpx python-dotenv 

COPY app/ ./app/
COPY static/ ./static/

EXPOSE 8082

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8082"]