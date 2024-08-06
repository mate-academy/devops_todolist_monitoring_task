from django.contrib import admin
from django.urls import include, path
from django_prometheus import exports


urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("metrics/", exports.ExportToDjangoView, name="prometheus-django-metrics"),
]
