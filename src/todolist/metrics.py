import time

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    disable_created_metrics,
    generate_latest,
)
from django.http import HttpResponse

disable_created_metrics()

METRICS_PATH = "/metrics"

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests handled by the application, labelled by method.",
    ["method"],
)

REQUEST_CREATED = Gauge(
    "http_requests_created_timestamp_seconds",
    "Unix timestamp in seconds when the HTTP request counter for each method was first created or reset.",
    ["method"],
)

_initialized_methods = set()


class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != METRICS_PATH:
            method = request.method
            if method not in _initialized_methods:
                REQUEST_CREATED.labels(method=method).set(time.time())
                _initialized_methods.add(method)
            REQUEST_COUNT.labels(method=method).inc()
        return self.get_response(request)


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
