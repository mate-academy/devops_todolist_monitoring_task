from django.http import HttpResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

HTTP_REQUESTS = Counter("http_requests", "Total HTTP requests", ["method"])


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != "/metrics":
            HTTP_REQUESTS.labels(method=request.method).inc()
        return self.get_response(request)


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)