from prometheus_client import Counter, generate_latest
from django.http import HttpResponse

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method'])


def metrics_view(request):
    REQUEST_COUNT.labels(method=request.method).inc()
    return HttpResponse(generate_latest(), content_type="text/plain; version=0.0.4; charset=utf-8")
