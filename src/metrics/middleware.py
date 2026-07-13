from .metrics import REQUEST_COUNT

class RequestMetricsMiddleware:
    """Counts GET and POST requests for Prometheus metrics."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ("GET", "POST") and request.path != "/metrics":
            REQUEST_COUNT.labels(method=request.method).inc()
        return self.get_response(request)