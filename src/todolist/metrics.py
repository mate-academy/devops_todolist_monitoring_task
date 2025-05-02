from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method']
)

def metrics(request):
    if request.method == "GET":
        http_requests_total.labels(method="GET").inc()
    elif request.method == "POST":
        http_requests_total.labels(method="POST").inc()

    return HttpResponse(generate_latest(), content_type='text/plain; version=0.0.4')