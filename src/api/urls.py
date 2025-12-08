from api import views
from api.views import metrics
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"todolists", views.TodoListViewSet)
router.register(r"todos", views.TodoViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("health", views.health, name="health"),
    path("ready", views.ready, name="ready"),
    path('metrics/', metrics)
]
