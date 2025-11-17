from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from django.http import HttpResponse
import time

# Лічильник HTTP-запитів з мітками "method" та "endpoint" (для кращої деталізації)
HTTP_REQUEST_COUNT = Counter(
    'todoapp_http_request_total',
    'Total HTTP requests, labeled by method and endpoint',
    ['method', 'endpoint']
)

# Gauge для часу створення метрик (час запуску)
REQUESTS_CREATED = Gauge(
    'todoapp_http_requests_created',
    'Unix timestamp when the HTTP request counters were created'
)
REQUESTS_CREATED.set(time.time())

def metrics_view(request):
    """
    Ендпоінт, який повертає всі зареєстровані метрики у форматі Prometheus.
    """
    return HttpResponse(
        generate_latest(REGISTRY),
        content_type=CONTENT_TYPE_LATEST
    )