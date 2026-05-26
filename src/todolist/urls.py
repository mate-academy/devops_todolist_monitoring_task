from django.contrib import admin
from django.urls import include, path
from todolist import views # <-- Переконайтесь, що цей імпорт вказує на ваш views.py

urlpatterns = [
    path("", include("lists.urls")),
    path("auth/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("metrics", views.metrics, name="metrics"), # <-- Додайте цей рядок
]