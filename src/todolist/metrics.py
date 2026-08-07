from django.http import HttpResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


http_requests_total = Counter(
    "todoapp_http_requests_total",
    "Total number of HTTP requests",
    ["method"]
)


def metrics_view(request):
    return HttpResponse(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST
    )
