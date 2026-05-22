# Step 2: Prometheus metrics implementation
# This file creates the /metrics endpoint and tracks HTTP requests

from prometheus_client import Counter, generate_latest, REGISTRY
from django.http import HttpResponse


# Step 3: Create counters for GET and POST requests
# These metrics track the total number of HTTP requests by method
# They will be exposed at the /metrics endpoint in Prometheus format
get_requests_counter = Counter(
    'http_get_requests_total',
    'Total number of GET requests',
    ['method']
)

post_requests_counter = Counter(
    'http_post_requests_total',
    'Total number of POST requests',
    ['method']
)


class PrometheusMetricsMiddleware:
    """
    Middleware to track GET and POST requests
    
    This middleware intercepts all HTTP requests and increments
    the appropriate counter based on the request method.
    It must be added to MIDDLEWARE in settings.py.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Track the request by incrementing the appropriate counter
        if request.method == 'GET':
            get_requests_counter.labels(method='GET').inc()
        elif request.method == 'POST':
            post_requests_counter.labels(method='POST').inc()
        
        response = self.get_response(request)
        return response


def metrics_view(request):
    """
    Step 2: View that returns Prometheus metrics at /metrics endpoint
    
    This view generates metrics in Prometheus exposition format.
    It returns all registered metrics including:
    - http_get_requests_total: Total GET requests
    - http_post_requests_total: Total POST requests
    - Plus default process and Python metrics
    """
    metrics = generate_latest(REGISTRY)
    return HttpResponse(metrics, content_type='text/plain; charset=utf-8')
