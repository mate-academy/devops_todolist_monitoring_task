from prometheus_client import Counter

REQUEST_COUNT = Counter(
    "todoapp_http_requests_total",
    "Total HTTP requests",
    ["method", "path"]
)

class PrometheusRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        method = request.method.upper()
        # считаем только GET/POST
        if method in ("GET", "POST"):
            # можно нормализовать path, чтобы не плодить уникальные значения
            path = request.path
            REQUEST_COUNT.labels(method=method, path=path).inc()

        return response
