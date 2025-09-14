from prometheus_client import Counter, Histogram
import time

# Define Prometheus metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

class PrometheusMiddleware:
    """
    Middleware to track HTTP requests for Prometheus metrics
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Record start time
        start_time = time.time()
        
        # Get the response
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Extract method and endpoint
        method = request.method
        endpoint = request.path
        
        # Update metrics
        http_requests_total.labels(method=method, endpoint=endpoint).inc()
        http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
        
        return response


