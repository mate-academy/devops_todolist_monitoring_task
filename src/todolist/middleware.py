from todolist.metrics import HTTP_REQUESTS_TOTAL


class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != "/metrics" and request.method in {"GET", "POST"}:
            HTTP_REQUESTS_TOTAL.labels(method=request.method).inc()

        return self.get_response(request)
