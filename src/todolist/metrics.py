from prometheus_client import Counter


HTTP_REQUESTS_TOTAL = Counter(
    "todoapp_http_requests_total",
    "Total number of HTTP requests",
    ["method"],
)

for method in ("GET", "POST"):
    HTTP_REQUESTS_TOTAL.labels(method=method)
