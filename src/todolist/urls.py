from django.contrib import admin
from django.urls import include, path
from todolist.metrics import metrics_view

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("metrics", metrics_view, name="metrics"),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]
