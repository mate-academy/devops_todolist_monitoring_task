from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

http_requests_total = Counter(
    "todo_http_requests_total",
    "Total number of HTTP requests",
    ["method"],
)


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method in ("GET", "POST") and request.path != "/metrics":
            http_requests_total.labels(method=request.method).inc()

        return response


def metrics_view(request):
    return HttpResponse(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )
