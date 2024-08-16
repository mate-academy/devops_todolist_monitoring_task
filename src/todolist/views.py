from prometheus_client import generate_latest, Counter
from django.http import HttpResponse


GET_REQUESTS = Counter("django_http_get_requests_total", "Total GET HTTP requests")
POST_REQUESTS = Counter("django_http_post_requests_total", "Total POST HTTP requests")


def metrics(request):
    if request.method == "GET":
        GET_REQUESTS.inc()
    elif request.method == "POST":
        POST_REQUESTS.inc()

    metrics_data = generate_latest()
    return HttpResponse(metrics_data, content_type="text/plain")