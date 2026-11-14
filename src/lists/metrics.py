from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

# Лічильник для Prometheus, який збирає GET та POST запити
REQUEST_COUNT = Counter(
    'todo_http_requests_total',
    'Total HTTP requests by method',
    ['method']
)

def metrics_view(request):
    """Ендпойнт /metrics, який віддає зібрані дані"""
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)

class PrometheusMiddleware:
    """Мідлваре для перехоплення та підрахунку всіх GET і POST запитів"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Не рахуємо сам шлях /metrics, щоб не створювати петлю
        if not request.path.startswith('/metrics'):
            if request.method in ['GET', 'POST']:
                REQUEST_COUNT.labels(method=request.method).inc()

        response = self.get_response(request)
        return response