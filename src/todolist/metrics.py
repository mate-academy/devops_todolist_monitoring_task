from prometheus_client import Counter, CONTENT_TYPE_LATEST, generate_latest
from django.http import HttpResponse

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method"],
)


class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ("GET", "POST"):
            REQUEST_COUNT.labels(method=request.method).inc()
        return self.get_response(request)


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)