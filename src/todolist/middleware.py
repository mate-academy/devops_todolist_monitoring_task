from .metrics import GET_REQUESTS, POST_REQUESTS

class MetricsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method == "GET":
            GET_REQUESTS.inc()

        elif request.method == "POST":
            POST_REQUESTS.inc()

        response = self.get_response(request)
        return response