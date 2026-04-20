from .metrics import REQUEST_COUNT

class RequestCountMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        method = request.method.upper()

        if method in ("GET", "POST"):
            path = request.path
            REQUEST_COUNT.labels(method=method, path=path).inc()

        return response