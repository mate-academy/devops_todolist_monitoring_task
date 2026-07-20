from prometheus_client import Counter

GET_REQUESTS = Counter(
    "http_get_requests_total",
    "Total number of GET requests"
)

POST_REQUESTS = Counter(
    "http_post_requests_total",
    "Total number of POST requests"
)