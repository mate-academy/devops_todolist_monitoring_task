from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


def metrics_view(request):
    """
    Віддає всі згенеровані метрики у форматі, сумісному з Prometheus.
    """
    metrics = generate_latest()
    return HttpResponse(metrics, content_type=CONTENT_TYPE_LATEST)

