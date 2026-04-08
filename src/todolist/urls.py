from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("metrics/", views.metrics_view, name="metrics"),
    path("admin/", admin.site.urls),
]
 