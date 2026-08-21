from django.http import HttpResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method"],
)


class MetricsMiddleware:
    """Count GET and POST requests for Prometheus scraping."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path != "/metrics" and request.method in ("GET", "POST"):
            http_requests_total.labels(method=request.method).inc()
        return response


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
