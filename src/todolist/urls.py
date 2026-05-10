from api.views import metrics # Не забудьте цей імпорт!
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("metrics/", metrics, name="prometheus-metrics"),
]