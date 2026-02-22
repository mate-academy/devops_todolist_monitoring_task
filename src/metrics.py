from prometheus_client import Counter, Gauge
import time

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method"]
)

APP_START_TIME = Gauge(
    "http_requests_created",
    "Application start time"
)

APP_START_TIME.set(time.time())