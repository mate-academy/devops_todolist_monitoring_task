from prometheus_client import Counter
from django.utils.deprecation import MiddlewareMixin

# Створюємо лічильники для GET і POST-запитів
GET_REQUESTS = Counter("django_http_get_requests_total", "Total number of HTTP GET requests")
POST_REQUESTS = Counter("django_http_post_requests_total", "Total number of HTTP POST requests")

class MetricsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "GET":
            GET_REQUESTS.inc()
        elif request.method == "POST":
            POST_REQUESTS.inc()
