from prometheus_client import Counter


HTTP_REQUESTS_TOTAL = Counter(
    "todoapp_http_requests",
    "Total number of HTTP requests",
    ["method"],
)
