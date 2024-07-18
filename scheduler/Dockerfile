FROM python:3.9-slim

WORKDIR /app

COPY . .

WORKDIR /app/scheduler

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "chain_tasks.py"]
