from django.http import HttpResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
