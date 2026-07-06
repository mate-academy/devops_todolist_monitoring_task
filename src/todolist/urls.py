from django.contrib import admin
from django.urls import include, path
from todolist.views import metrics_view

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("metrics", metrics_view, name="metrics"),
]
