from .metrics import http_requests_total

class RequestCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != "/metrics":
            http_requests_total.labels(method=request.method).inc()

        response = self.get_response(request)
        return response
