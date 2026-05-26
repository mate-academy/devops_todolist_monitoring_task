from prometheus_client import Counter, generate_latest, Gauge
from django.http import HttpResponse
import time

# Define request counters.
# Ці лічильники будуть інкрементуватися лише при зверненні до /metrics.
get_request_counter = Counter('get_requests_total', 'Total number of GET requests to /metrics endpoint')
post_request_counter = Counter('post_requests_total', 'Total number of POST requests to /metrics endpoint')

# Метрика часу створення/перезапуску додатка.
# Ця метрика фіксує час запуску Python процесу.
app_startup_time = Gauge('http_requests_creation_time', 'Timestamp when the application started (Unix timestamp)')
app_startup_time.set(time.time()) # Встановлюємо значення при завантаженні модуля

def metrics(request):
    if request.method == 'GET':
        get_request_counter.inc()
    elif request.method == 'POST':
        post_request_counter.inc()

    return HttpResponse(generate_latest(), content_type='text/plain; version=0.0.4')