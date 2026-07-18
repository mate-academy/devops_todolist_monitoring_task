from prometheus_client import Counter

HTTP_REQUESTS_TOTAL = Counter('django_http_requests_total', 'Total number of HTTP request to the Django application', ['method'])

class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method

        if method in ['GET', 'POST']:
            HTTP_REQUESTS_TOTAL.labels(method=method).inc()
        response = self.get_response(request)
        return response