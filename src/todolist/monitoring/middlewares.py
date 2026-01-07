import time
from prometheus_client import Counter, Histogram  # Рекомендую Histogram для задержки

REQUEST_COUNT = Counter(
    "django_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "django_http_requests_latency_seconds",
    "HTTP Request latency in seconds",
    ["method", "endpoint"]
)


class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/metrics':
            return self.get_response(request)

        start_time = time.time()

        response = self.get_response(request)

        REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

        resp_time = time.time() - start_time
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(resp_time)

        return response
