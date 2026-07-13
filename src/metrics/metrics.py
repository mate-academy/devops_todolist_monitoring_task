from prometheus_client import Counter

REQUEST_COUNT = Counter(
    "django_http_requests_total",
    "Total number of HTTP requests by method",
    ["method"],
)