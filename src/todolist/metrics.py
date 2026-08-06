from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from django.http import HttpResponse

REQUEST_COUNT = Counter(
    "django_http_requests_total",
    "Total number of HTTP requests",
    ["method"],
)


class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        REQUEST_COUNT.labels(method=request.method).inc()
        return response


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
