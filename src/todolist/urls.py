from django.contrib import admin
from django.urls import include, path
from .metrics import metrics_view

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    # Step 2: Add /metrics endpoint (not api/metrics)
    # This endpoint exposes Prometheus metrics for monitoring
    path("metrics", metrics_view),
]
