from django.utils.deprecation import MiddlewareMixin
from .metrics import (get_request_counter, post_request_counter)

class RequestMetricsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'GET':
            get_request_counter.inc()
        elif request.method == 'POST':
            post_request_counter.inc()
        return None