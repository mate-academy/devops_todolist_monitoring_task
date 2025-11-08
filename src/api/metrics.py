from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse
import time

# Лічильник HTTP-запитів з лейблом "method"
REQUEST_COUNT = Counter(
    'todoapp_http_requests_total',
    'Total HTTP requests',
    ['method']
)

# Gauge для часу створення метрик (один раз при імпорті)
REQUESTS_CREATED = Gauge(
    'todoapp_http_requests_created',
    'Unix timestamp when the HTTP request counters were created'
)
REQUESTS_CREATED.set(time.time())

# View для /metrics
def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)