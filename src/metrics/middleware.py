import time
from prometheus_client import Counter, Gauge

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method"]
)

http_requests_created = Gauge(
    "http_requests_created",
    "Time when the HTTP request counters were created or reset"
)
http_requests_created.set(time.time())

EXCLUDED_PATHS = ("/metrics", "/api/health", "/api/ready")

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(EXCLUDED_PATHS):
            http_requests_total.labels(method=request.method).inc()

        return self.get_response(request)