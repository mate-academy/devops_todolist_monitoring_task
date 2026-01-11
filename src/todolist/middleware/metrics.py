from prometheus_client import Counter

http_requests_total = Counter(
    'todoapp_http_requests_total',
    'Total number of HTTP requests processed by the app',
    ['method', 'endpoint']
)


class MetricsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = ['/metrics', '/api/health', '/api/ready']

        path = request.path.rstrip('/')
        method = request.method.upper()

        if path not in excluded_paths and method in ('GET', 'POST'):

            http_requests_total.labels(method=method, endpoint=path).inc()

        response = self.get_response(request)
        return response
