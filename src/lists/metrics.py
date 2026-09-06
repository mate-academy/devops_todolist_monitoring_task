from prometheus_client import Counter

http_requests_total = Counter(
    "todo_http_requests_total",
    "Total number of HTTP requests",
    ["method"],
)
