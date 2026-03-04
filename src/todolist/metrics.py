from prometheus_client import Counter


HTTP_REQUESTS_TOTAL = Counter(
    "todoapp_http_requests_total",
    "Total number of HTTP requests by method.",
    ["method"],
)
