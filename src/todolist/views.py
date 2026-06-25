from django.http import HttpResponse
from prometheus_client import Counter, Gauge, generate_latest


REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method']
)

startup_time = Gauge('http_requests_startup_time', 'Application startup time')
startup_time.set_to_current_time()



class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        REQUEST_COUNTER.labels(
            method=request.method
        ).inc()

        return self.get_response(request)

def metrics(request):
    return HttpResponse(
        generate_latest(),
        content_type='text/plain'
    )

