from .metrics import http_requests_total

class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method in ["GET", "POST"]:
            http_requests_total.labels(method=request.method).inc()
        return response
