from urllib import request

from prometheus_client import Counter

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method"]
)

EXCLUDED_PATHS = ("/metrics", "/api/health", "/api/ready")

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(EXCLUDED_PATHS):
            http_requests_total.labels(method=request.method).inc()

        return self.get_response(request)

