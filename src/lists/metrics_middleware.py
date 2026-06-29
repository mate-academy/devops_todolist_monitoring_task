from prometheus_client import Counter

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests by method.',
    ['method']
)


class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method

    
        if method in ['GET', 'POST']:
            REQUEST_COUNT.labels(method=method).inc()

        response = self.get_response(request)
        return response