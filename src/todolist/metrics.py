from prometheus_client import Counter, generate_latest
from django.http import HttpResponse


GET_REQUESTS = Counter('http_get_requests_total', 'Total number of GET requests')
POST_REQUESTS = Counter('http_post_requests_total', 'Total number of POST requests')

def metrics_view(request):
    if request.method == "GET":
        GET_REQUESTS.inc()
    elif request.method == "POST":
        POST_REQUESTS.inc()

    metrics_data = generate_latest()
    return HttpResponse(metrics_data, content_type="text/plain; version=0.0.4; charset=utf-8")
