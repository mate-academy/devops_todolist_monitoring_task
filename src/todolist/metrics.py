from prometheus_client import Counter, Histogram
import time
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Define metrics
REQUEST_COUNT = Counter(
    'django_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'django_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.path
        ).observe(time.time() - start_time)
        
        return response 

def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST) 