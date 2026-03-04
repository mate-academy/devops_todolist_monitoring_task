from django.contrib import admin
from django.urls import include, path

from api import views as api_views

urlpatterns = [
    path("", include("lists.urls")),
    path("metrics", api_views.metrics, name="metrics"),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]
