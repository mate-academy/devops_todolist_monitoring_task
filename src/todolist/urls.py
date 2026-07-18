from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .views import metrics_view

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("metrics", metrics_view, name="metrics"),
]