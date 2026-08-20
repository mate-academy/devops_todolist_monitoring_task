# api/middleware.py
import logging
from prometheus_client import Counter
logger = logging.getLogger(__name__)
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method'])
class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        logger.info(f"Middleware called for {request.method} {request.path}")
        http_requests_total.labels(method=request.method).inc()
        return self.get_response(request)
