from django.contrib import admin
from django.urls import include, path
from api.views import metrics  # додали імпорт

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),

    # Prometheus metrics endpoint
    path("metrics", metrics, name="metrics"),

    path("admin/", admin.site.urls),
]
