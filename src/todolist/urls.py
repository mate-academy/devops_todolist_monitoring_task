from django.contrib import admin
from django.urls import include, path
from .metrics import todolist_metrics

from src.lists.views import todolist

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("metrics/", todolist_metrics)
]
