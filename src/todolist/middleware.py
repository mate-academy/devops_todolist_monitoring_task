from prometheus_client import Counter

# Лічильники для GET і POST
get_requests_total = Counter("http_requests_get_total", "Total number of GET requests")
post_requests_total = Counter("http_requests_post_total", "Total number of POST requests")

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET":
            get_requests_total.inc()
        elif request.method == "POST":
            post_requests_total.inc()

        response = self.get_response(request)
        return response