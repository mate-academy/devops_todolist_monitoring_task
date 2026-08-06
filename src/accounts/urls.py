from django.urls import path

from accounts import views
from metric import metrics_view

app_name = "auth"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('metrics', metrics_view, name='metrics'),
]
