from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

def metrics_view(request):
    metrics_data = generate_latest()
    return HttpResponse(metrics_data, content_type=CONTENT_TYPE_LATEST)