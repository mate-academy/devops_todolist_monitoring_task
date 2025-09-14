from django.contrib import admin
from django.urls import include, path
from monitoring.metrics import metrics_view

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),

    # /metrics без редіректів + дубль зі слешем
    path("metrics", metrics_view),
    path("metrics/", metrics_view),
]
