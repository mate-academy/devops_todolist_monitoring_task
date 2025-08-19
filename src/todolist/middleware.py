from prometheus_client import Counter

requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests', ['method']
    )


class PrometheusMiddleware:
    """
    Middleware to track HTTP GET and POST requests for Prometheus monitoring.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        requests_total.labels(request.method).inc()
        response = self.get_response(request)
        return response
