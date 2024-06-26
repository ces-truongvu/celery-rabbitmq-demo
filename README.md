# Celery with RabbitMQ and Flower

This repository contains a Docker Compose setup for running Celery with RabbitMQ as the message broker and Flower for monitoring. The setup includes:

- RabbitMQ: A message broker to handle the task queue.
- Celery Worker: Executes Celery tasks.
- Celery Scheduler: Emit tasks.
- Flower: A real-time monitoring tool for Celery.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Clone repository & start docker-compose

```sh
git clone https://github.com/ces-truongvu/celery-rabbitmq-demo

cd celery-rabbitmq-demo
docker-compose up -d
```

### Capture image

```sh
docker up scheduler
```

After that, you should find an image named `google.png` in the scheduler folder
