from django.utils.deprecation import MiddlewareMixin

from .requests_counter import count_requests


class RequestCountingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        count_requests(request)
