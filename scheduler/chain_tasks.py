# import os
# from celery import Celery, chain
#
# # Ensure the RabbitMQ URL is set correctly in the environment
# rabbitmq_url = os.getenv('RABBITMQ_URL', 'pyamqp://user:password@rabbitmq:5672//')
#
# # The Celery app should match the name defined in tasks.py
# app = Celery('tasks', broker=rabbitmq_url, backend='rpc://')
#
# # Define the task configuration
# task_config = {
#     'url': 'https://google.com',
#     'screenshot_path': 'google.png',
#     'thumbnail_path': 'google_thumb.jpg'
# }
#
# # Create the chain of tasks
# task_chain = chain(
#     app.signature('tasks.run_visual_regression_test', args=(task_config)),
#     app.signature('tasks.create_thumbnail', args=(task_config['screenshot_path'], 
#                                                   task_config['thumbnail_path']))
# )
#
# # Send the chain of tasks
# result = task_chain.apply_async()
# print(result)
# if result:
#     print(f" [x] Sent task chain with ID: {result.id}")
# else:
#     print("Failed to send task chain")

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

    task_config = {
        'url': 'https://google.com',
        'screenshot_path': 'google.png',
        'thumbnail_path': 'google.png'
    }

    chain_message = {
        'id': str(uuid.uuid4()),
        'task': 'tasks.capture_resize_google',
        'args': [task_config],
        'kwargs': {},
        'retries': 1,
        'eta': None
    }

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(chain_message),
        properties=pika.BasicProperties(
            content_type='application/json',
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent ")

    connection.close()
except Exception as e:
    print(f"Error: {e}")
