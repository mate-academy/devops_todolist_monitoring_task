from __future__ import annotations
import time
from django.http import HttpResponse
from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY,
)

# ── reloader-safe: створюємо метрики лише один раз ────────────────────────────
if "REQUESTS_TOTAL" not in globals():
    REQUESTS_TOTAL = Counter(
        "todoapp_http_requests_total",
        "Total number of HTTP requests",
        labelnames=("method",),
        registry=REGISTRY,
    )

if "APP_START_TIME" not in globals():
    APP_START_TIME = Gauge(
        "todoapp_app_start_time_seconds",
        "App start time in unix seconds",
        registry=REGISTRY,
    )
    # ставимо значення лише якщо ще не встановлено
    try:
        if APP_START_TIME._value.get() == 0:  # noqa: SLF001 (внутрішній атрибут ок для простоти)
            APP_START_TIME.set(time.time())
    except Exception:
        APP_START_TIME.set(time.time())

def metrics_view(_request):
    # віддаємо метрики з дефолтного реєстру
    data = generate_latest(REGISTRY)
    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
