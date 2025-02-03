from django.contrib import admin
from django.urls import include, path
from django.urls import path
from prometheus_client import make_wsgi_app
from django.http import HttpResponse
from wsgiref.simple_server import make_server

def prometheus_metrics(request):
    """Serve Prometheus metrics."""
    return HttpResponse(make_wsgi_app()(request.environ, lambda s, h: None))

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("metrics/", prometheus_metrics, name="metrics"),
]
