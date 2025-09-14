from __future__ import annotations
from .metrics import REQUESTS_TOTAL

class PrometheusRequestCounterMiddleware:
    """Рахує тільки GET/POST, ігнорує /metrics; інкремент після відповіді."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith("/metrics"):
            return response

        if request.method in ("GET", "POST"):
            # якщо хочеш рахувати лише успішні — розкоментуй наступний рядок
            # if 200 <= getattr(response, "status_code", 200) < 400:
            REQUESTS_TOTAL.labels(method=request.method).inc()

        return response
