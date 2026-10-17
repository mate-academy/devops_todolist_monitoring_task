from prometheus_client import Counter

http_requests = Counter(
    "http_requests",
    "Total number of HTTP requests",
    ["method"]
)
