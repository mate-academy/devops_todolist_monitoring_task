from prometheus_client import Counter, Gauge

# Counter that counts HTTP requests grouped by method and path
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path"]
)

# Gauge: timestamp when counters were created (helps detect restarts)
HTTP_REQUESTS_CREATED_TIME = Gauge(
    "http_requests_created_time",
    "Time when HTTP request counters were created or reset (unix seconds)"
)

# Set gauge value when Django loads
HTTP_REQUESTS_CREATED_TIME.set_to_current_time()


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # increment the request counter
        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            path=request.path
        ).inc()

        return self.get_response(request)
