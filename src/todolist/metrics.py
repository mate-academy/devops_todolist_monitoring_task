from django.http import HttpResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# Створюємо метрики-лічильники для GET і POST запитів
GET_REQUESTS = Counter('http_get_requests_total', 'Total number of GET requests')
POST_REQUESTS = Counter('http_post_requests_total', 'Total number of POST requests')

def metrics_view(request):
    # Збільшуємо лічильник залежно від типу запиту
    if request.method == 'GET':
        GET_REQUESTS.inc()
    elif request.method == 'POST':
        POST_REQUESTS.inc()

    # Віддаємо метрики у форматі, який розуміє Prometheus
    metrics_data = generate_latest()
    return HttpResponse(metrics_data, content_type=CONTENT_TYPE_LATEST)