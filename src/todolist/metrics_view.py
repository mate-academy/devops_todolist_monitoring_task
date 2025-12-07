from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


def metrics(request):
    data = generate_latest()
    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
