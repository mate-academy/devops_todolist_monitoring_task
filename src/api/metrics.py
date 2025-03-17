from prometheus_client import Counter, generate_latest
from django.http import HttpResponse

# Лічильники Prometheus для GET та POST запитів
GET_REQUEST_COUNT = Counter("http_get_requests_total", "Total GET requests")
POST_REQUEST_COUNT = Counter("http_post_requests_total", "Total POST requests")

def metrics(request):
    # Ця функція буде повертати метрики Prometheus
    return HttpResponse(generate_latest(), content_type="text/plain")
