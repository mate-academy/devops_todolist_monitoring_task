from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests', ['method'])

def some_view(request):
    REQUEST_COUNTER.labels(method=request.method).inc()

def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)