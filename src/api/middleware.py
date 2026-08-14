from api.metrics import HTTP_REQUESTS_TOTAL

class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method in ("GET", "POST"):
            HTTP_REQUESTS_TOTAL.labels(method=request.method).inc()
        return response