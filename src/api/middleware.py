from .metrics import HTTP_REQUEST_COUNT


class RequestCounterMiddleware:
    """
    Middleware для інкрементування лічильника HTTP-запитів.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        endpoint = request.path

        # Інкрементуємо лічильник, використовуючи метод та шлях
        HTTP_REQUEST_COUNT.labels(method=request.method, endpoint=endpoint).inc()

        return response