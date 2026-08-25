from prometheus_client import Counter

HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method']
)

class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        HTTP_REQUESTS_TOTAL.labels(method=request.method).inc()
        return self.get_response(request)