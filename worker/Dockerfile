FROM python:3.12-bookworm

RUN pip install playwright Pillow && \
  playwright install --with-deps

WORKDIR /app

COPY . .

WORKDIR /app/worker

RUN pip install --no-cache-dir -r requirements.txt

# CMD ["celery", "-A", "tasks", "worker", "--loglevel=info", "--queues=tasks"]

