import time
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'http_status']
)

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.method in ("GET", "POST"):
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.path,
                http_status=response.status_code
            ).inc()

        return response