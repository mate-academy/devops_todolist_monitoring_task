from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY


def metrics_view(request):
    """
    Exports Prometheus metrics collected by the default registry.
    """

    data = generate_latest(REGISTRY)

    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
