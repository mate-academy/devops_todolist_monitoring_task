import time
from prometheus_client import Gauge
from django.http import HttpResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method"]
)


APP_START_TIME = Gauge(
    'app_start_time_seconds',
    'Time when the app was started'
)
APP_START_TIME.set(time.time())


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)