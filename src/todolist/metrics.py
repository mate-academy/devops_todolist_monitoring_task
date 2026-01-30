from prometheus_client import Counter

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method"]
)
