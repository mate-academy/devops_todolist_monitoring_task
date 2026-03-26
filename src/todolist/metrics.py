from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest


REQUEST_COUNTER = Counter(
    "todoapp_http_requests",
    "Total number of HTTP requests handled by the todo app.",
    ("method",),
)

TRACKED_METHODS = {"GET", "POST"}
EXCLUDED_PATHS = {"/metrics"}


class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method in TRACKED_METHODS and request.path not in EXCLUDED_PATHS:
            REQUEST_COUNTER.labels(method=request.method).inc()

        return response


def get_metrics_response():
    return generate_latest(), CONTENT_TYPE_LATEST
