import time

from django.http import HttpResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest


http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method"],
)

http_requests_created_at = Gauge(
    "http_requests_created_at",
    "Unix timestamp when the HTTP metrics were initialized",
)
http_requests_created_at.set(time.time())


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ("GET", "POST"):
            http_requests_total.labels(method=request.method).inc()
        return self.get_response(request)


def metrics(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
