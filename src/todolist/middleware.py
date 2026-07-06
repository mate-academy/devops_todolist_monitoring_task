from .metrics import REQUEST_COUNTER

EXCLUDED_PATHS = ['/metrics/', '/api/health', '/api/ready']

class PrometheusMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not any(request.path.startswith(path) for path in EXCLUDED_PATHS):
            REQUEST_COUNTER.labels(method=request.method).inc()
        
        response = self.get_response(request)
        return response