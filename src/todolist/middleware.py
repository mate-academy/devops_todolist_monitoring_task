from prometheus_client import Counter

REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method']
)

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        def __call__(self, request):
            REQUEST_COUNTER.labels(method=request.method).inc()
            response = self.get_response(request)
            return response