from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse
import time


HTTP_REQUESTS_TOTAL = Counter(
    "todoapp_http_requests_total",          # імʼя метрики в Prometheus
    "Total HTTP requests by method",       # опис
    ["method"],                            # лейбл: method=get/post
)


HTTP_REQUESTS_CREATED_AT = Gauge(
    "todoapp_http_requests_created_at",
    "Unix time when HTTP request counters were initialised",
)


HTTP_REQUESTS_CREATED_AT.set(time.time())


def metrics_view(request):
    data = generate_latest()
    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
