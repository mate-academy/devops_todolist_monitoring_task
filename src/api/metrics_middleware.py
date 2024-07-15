from prometheus_client import Counter

# Counters for GET and POST requests
get_counter = Counter("http_get_requests_total", "Total number of GET requests")
post_counter = Counter("http_post_requests_total", "Total number of POST requests")

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Increment the appropriate counter
        if request.method == "GET":
            get_counter.inc()
        elif request.method == "POST":
            post_counter.inc()

        response = self.get_response(request)
        return response