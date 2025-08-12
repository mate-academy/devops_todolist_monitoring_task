from prometheus_client import Counter

http_requests_total = Counter(
    'todoapp_http_requests_total',
    'Total HTTP requests',
    ['method']
)

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method.upper()
        if method in ['GET', 'POST']:
            http_requests_total.labels(method=method).inc()

        response = self.get_response(request)
        return response
