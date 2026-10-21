from .views import http_requests_total

class PrometheusRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ("GET", "POST") and request.path != "/metrics/":
            http_requests_total.labels(method=request.method, endpoint=request.path).inc()

        return self.get_response(request)