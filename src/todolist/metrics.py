from prometheus_client import Counter, generate_latest
from django.http import HttpResponse

HTTP_REQUESTS = Counter(
    'http_requests_total',
    'Total number of HTTP requests.',
    ['method']
)


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['GET', 'POST']:
            HTTP_REQUESTS.labels(method=request.method).inc()

        response = self.get_response(request)

        return response


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type="text/plain")
