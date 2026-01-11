from prometheus_client import Counter

# Лічильники HTTP-запитів за методом
http_requests_total = Counter(
    'todoapp_http_requests_total',
    'Total number of HTTP requests processed by the app',
    ['method', 'endpoint']
)


class MetricsMiddleware:
    """
    Middleware, що інкрементує лічильники HTTP-запитів GET та POST для кожного запиту,
    окрім запитів до ендпоінту /metrics.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Список шляхів, які ми НЕ хочемо рахувати в бізнес-метриках
        excluded_paths = ['/metrics', '/api/health', '/api/ready']

        path = request.path.rstrip('/')

        # Рахуємо лише якщо це не системний запит
        if path not in excluded_paths:
            method = request.method.upper()
            # Додаємо label 'path', щоб у Grafana бачити, куди саме ходять люди
            http_requests_total.labels(method=method, endpoint=path).inc()

        response = self.get_response(request)
        return response
