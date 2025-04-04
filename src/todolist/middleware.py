from .urls import  http_requests_total, http_requests_last_time
import time
import logging


logger = logging.getLogger(__name__)

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        http_requests_total.labels(method=request.method).inc()
        current_time = time.time()
        http_requests_last_time.labels(method=request.method).set(current_time)
        logger.info(f"Set http_requests_last_time for {request.method} to {current_time}")
        response = self.get_response(request)
        return response