from todolist.metrics import HTTP_REQUESTS_TOTAL
from django.utils.deprecation import MiddlewareMixin


class PrometheusMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.path.startswith('/metrics'):
            method = request.method
            endpoint = request.path
            HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint).inc()

        return None