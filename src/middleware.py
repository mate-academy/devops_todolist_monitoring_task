from metrics import HTTP_REQUESTS

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ["GET", "POST"]:
            HTTP_REQUESTS.labels(method=request.method).inc()

        response = self.get_response(request)
        return response