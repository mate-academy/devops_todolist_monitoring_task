from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY

def metrics_view(request):
    """
    Exports Prometheus metrics collected by the default registry.
    """
    # Generate the latest metrics data payload
    data = generate_latest(REGISTRY)
    
    # Return the metrics with the required Prometheus content type
    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
