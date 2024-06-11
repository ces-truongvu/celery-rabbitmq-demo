FROM python:3.9-slim

WORKDIR /app

COPY . .

WORKDIR /app/worker

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]

