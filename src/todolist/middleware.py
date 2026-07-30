from todolist.metrics import HTTP_REQUESTS_TOTAL


EXCLUDED_PATHS = {
    "/metrics",
    "/api/health",
    "/api/ready",
}


class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.path not in EXCLUDED_PATHS
            and request.method in {"GET", "POST"}
        ):
            HTTP_REQUESTS_TOTAL.labels(method=request.method).inc()

        return response