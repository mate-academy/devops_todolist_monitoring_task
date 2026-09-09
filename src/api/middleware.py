from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)


class MetricsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        http_requests_total.labels(method=request.method, endpoint=request.path).inc()


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
