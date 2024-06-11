from celery import Celery
from playwright.sync_api import sync_playwright
import os

rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://user:password@localhost:5672/')

app = Celery('tasks', broker=rabbitmq_url)

@app.task
def run_visual_regression_test(test_config):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Example test: navigate to a page and take a screenshot
        page.goto(test_config['url'])
        page.screenshot(path=test_config['screenshot_path'])
        
        browser.close()
