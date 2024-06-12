
import pika
import json
import os
import uuid

rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://user:password@rabbitmq:5672//')

queue_name = 'tasks'  # Use the default Celery queue

try:
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    task = {
        'url': 'https://google1.com',
        'screenshot_path': 'google.png'
    }

    message = {
        'task': 'tasks.run_visual_regression_test',
        'id': str(uuid.uuid4()),
        'args': [task],
        'kwargs': {},
        'retries': 1,
        'eta': None
    }

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            content_type='application/json',
            delivery_mode=2,  # make message persistent
        ))
    print(f" [x] Sent {task}")

    connection.close()
except Exception as e:
    print(f"Error: {e}")
