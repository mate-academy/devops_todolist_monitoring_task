from prometheus_client import Counter

http_requests_total = Counter(
    "todoapp_http_requests_total",
    "Total HTTP requests",
    ["method"]
)