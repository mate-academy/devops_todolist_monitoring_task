from .metrics import HTTP_REQUESTS_TOTAL


class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method.upper()

        if method in ("GET", "POST"):
            HTTP_REQUESTS_TOTAL.labels(method=method.lower()).inc()

        response = self.get_response(request)
        return response
