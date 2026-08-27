import time
from prometheus_client import Counter, Gauge

HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method']
)
HTTP_REQUESTS_CREATED_TIME = Gauge(
    "http_requests_created",
    "Time when HTTP request counters were created or reset",
)

HTTP_REQUESTS_CREATED_TIME.set(time.time())

class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        HTTP_REQUESTS_TOTAL.labels(method=request.method).inc()
        return self.get_response(request)
