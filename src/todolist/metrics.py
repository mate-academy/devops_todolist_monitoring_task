from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

REQUEST_COUNTER = Counter(
    'django_http_requests_total',
    'Total HTTP requests by method and path',
    ['method']
)

def metrics(request):
    if request.method == "GET":
        REQUEST_COUNTER.labels(method="GET").inc()
    elif request.method == "POST":
        REQUEST_COUNTER.labels(method="POST").inc()

    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)