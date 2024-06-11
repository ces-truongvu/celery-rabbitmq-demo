import pika
import json
import os

rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://user:password@localhost:5672/')
queue_name = 'tasks'

connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
channel = connection.channel()

channel.queue_declare(queue=queue_name, durable=True)

task = {
    'url': 'https://google.com',
    'screenshot_path': 'google.png'
}

channel.basic_publish(
    exchange='',
    routing_key=queue_name,
    body=json.dumps(task),
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))

print(f" [x] Sent {task}")
connection.close()
