from todolist.metrics import track_http_request


class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/metrics"):
            track_http_request(request.method)
        return response
