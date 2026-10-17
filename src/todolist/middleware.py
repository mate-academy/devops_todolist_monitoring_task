from .metrics import http_requests


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ("GET", "POST") and request.path != "/metrics":
            http_requests.labels(method=request.method).inc()

        return self.get_response(request)
