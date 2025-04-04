from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from prometheus_client import generate_latest, Counter, Gauge


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type='text/plain')


http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method']
)


http_requests_last_time = Gauge(
    'http_requests_last_time',
    'Time of the last HTTP request',
    ['method']
)

def test_view(request):
    return HttpResponse("Test endpoint works!")


urlpatterns = [
    path("test/", test_view),
    path("metrics/", metrics_view),
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]
