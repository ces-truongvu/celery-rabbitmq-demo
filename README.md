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

### Access flower

Open browser and go to `http://localhost:5555` to access flower dashboard.

### Modify Worker

After modify worker you need to restart the worker container, here is the command:

```
docker-compose stop worker && docker-compose rm -f worker && docker-compose up -d worker && docker-compose logs -f worker
```

### Capture image by activate the scheduler

```sh
docker up scheduler
```

After that, you should find an image named `google.png` and `google_thumb.jpg` in the worker folder

### Multi workers

Open `docker-compose.yml` and duplicated worker service, you will see one scheduler can be run on multi worker. This is the power of Celery.
