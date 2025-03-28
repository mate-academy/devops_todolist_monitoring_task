from prometheus_client import generate_latest
from django.http import HttpResponse

def metrics_view(request):
    """Expose Prometheus metrics, including log counters."""
    metrics = generate_latest()  # Generate all Prometheus metrics
    return HttpResponse(metrics, content_type='text/plain')