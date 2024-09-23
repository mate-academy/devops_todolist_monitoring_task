from prometheus_client import Counter, generate_latest
from django.http import HttpResponse
import os
from dotenv import load_dotenv

load_dotenv()

get_request_counter = Counter('get_requests_total', 'Total number of GET requests')
post_request_counter = Counter('post_requests_total', 'Total number of POST requests')


def metrics(request):
    if request.method == 'GET':
        get_request_counter.inc()
    elif request.method == 'POST':
        post_request_counter.inc()

    return HttpResponse(generate_latest(), content_type='text/plain; version=0.0.4')

SECRET_KEY = os.getenv('SECRET_KEY')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
