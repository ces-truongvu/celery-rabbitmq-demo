from celery import Celery
import logging
import os
from PIL import Image
from playwright.sync_api import sync_playwright

# Configure the logger
logging.basicConfig(level=logging.INFO, format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s')
logger = logging.getLogger(__name__)

rabbitmq_url = os.getenv('RABBITMQ_URL', 'pyamqp://user:password@localhost:5672//')

app = Celery('tasks', broker=rabbitmq_url, backend='rpc://')
# Celery configuration
app.conf.update(
    task_default_queue='tasks',  # Set the default queue
    task_routes={
        'tasks.capture_resize_google': {'queue': 'tasks'},
    },
    task_default_exchange='tasks',
    task_default_exchange_type='direct',
    task_default_routing_key='tasks',
)

@app.task()
def capture_resize_google(args):
    # Wrap initial_input in a tuple
    res=task_one.apply_async((args,), link=task_two.s())

    # Wait for the chain to complete and get the result
    try:
        print((res))
        print(res.ready())
        print(res.status)
        print(res.result)
    except Exception as e:
        logger.error(f"Error getting chain result: {e}")

@app.task()
def task_one(args):
    try:
        logger.info(f"task_one received input: {args}")

        screenshot_path = args['screenshot_path']
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Example test: navigate to a page and take a screenshot
            page.goto(args['url'])
            page.screenshot(path=screenshot_path)
            
            browser.close()
        # Ensure the return value is JSON serializable
        return args['screenshot_path']
    except Exception as e:
        logger.error(f"Error in task_one: {e}")
        raise

@app.task()
def task_two(args):
    try:
        logger.info(f"task_two received input: {args}")

        with Image.open(args) as img:
            thumb_path = 'google_thumb.jpg'
            img.thumbnail(size=(128, 128))
            img.save(thumb_path, "JPEG")
        return thumb_path
    except Exception as e:
        logger.error(f"Error in task_two: {e}")
        raise

# This area is for testing
# dcupd && python tasks.py
# app.autodiscover_tasks(['__main__'])
#
# if __name__ == '__main__':
#     initial_input = {
#         'url': 'https://google.com',
#         'screenshot_path': 'google.png'
#     }
#
#     # Wrap initial_input in a tuple
#     res=task_one.apply_async((initial_input,), link=task_two.s())
#
#     # Wait for the chain to complete and get the result
#     try:
#         print((res))
#         print(res.ready())
#         print(res.status)
#         print(res.result)
#     except Exception as e:
#         logger.error(f"Error getting chain result: {e}")
