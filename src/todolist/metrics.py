from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

# Define Prometheus Counters
GET_REQUEST = Counter("http_get_request_total", "Total number of GET requests")

# Metrics Endpoint
def todolist_metrics(request):
    if request.method == "GET":
        GET_REQUEST.inc()

    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)