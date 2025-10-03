from .metrics import REQUEST_COUNT

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        REQUEST_COUNT.labels(method=request.method).inc()
        response = self.get_response(request)
        return response