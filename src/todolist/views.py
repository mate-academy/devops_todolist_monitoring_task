from prometheus_client import Counter, generate_latest
from django.http import HttpResponse


get_request_counter = Counter('get_requests_total', 'Total number of GET requests')
post_request_counter = Counter('post_requests_total', 'Total number of POST requests')

def metrics(request):
    if request.method == 'GET':
        get_request_counter.inc()
    elif request.method == 'POST':
        post_request_counter.inc()

    return HttpResponse(generate_latest(), content_type='text/plain; version=0.0.4')
