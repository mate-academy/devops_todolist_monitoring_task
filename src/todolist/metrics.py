from django.http import HttpResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest


HTTP_REQUESTS = Counter(
    "todo_http_requests_total",
    "Total number of HTTP requests",
    ["method"],
)

# Створюємо обидві серії відразу, навіть поки їх значення дорівнює нулю.
HTTP_REQUESTS.labels(method="GET")
HTTP_REQUESTS.labels(method="POST")


def metrics_view(request):
    return HttpResponse(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )