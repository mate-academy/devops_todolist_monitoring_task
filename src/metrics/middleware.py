from prometheus_client import Counter

get_requests_total = Counter('http_get_requests_total', 'Total number of GET requests')
post_requests_total = Counter('http_post_requests_total', 'Total number of POST requests')


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET':
            get_requests_total.inc()
        elif request.method == 'POST':
            post_requests_total.inc()
        return self.get_response(request)
