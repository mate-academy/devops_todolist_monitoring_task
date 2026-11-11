from django.http import HttpResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# Counter for tracking HTTP requests by method (GET and POST)
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method"],
)

# Initialize GET and POST counters so they appear immediately in metrics
HTTP_REQUESTS_TOTAL.labels(method="GET")
HTTP_REQUESTS_TOTAL.labels(method="POST")


def metrics_view(request):
    """View to expose metrics in Prometheus-compatible format."""
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)


class MetricsMiddleware:
    """Middleware to count GET and POST requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ["GET", "POST"]:
            HTTP_REQUESTS_TOTAL.labels(method=request.method).inc()
        response = self.get_response(request)
        return response
