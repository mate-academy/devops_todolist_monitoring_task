from django.contrib import admin
from django.urls import include, path

from todolist.metrics import metrics

urlpatterns = [
    path("metrics/", metrics, name="metrics"),
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]
