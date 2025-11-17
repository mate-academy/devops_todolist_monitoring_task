from django.contrib import admin
from django.urls import include, path

# ІМПОРТ: Підключаємо нашу функцію metrics_view з новоствореного модуля api.metrics
from api.metrics import metrics_view

urlpatterns = [
    # ДОДАНО МАРШРУТ: Створюємо endpoint /metrics
    path("metrics", metrics_view, name="metrics"),

    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]