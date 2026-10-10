from .metrics import HTTP_REQUESTS


class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ("GET", "POST"):
            HTTP_REQUESTS.labels(method=request.method).inc()

        return self.get_response(request)