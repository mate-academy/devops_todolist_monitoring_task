# urls.py

from django.urls import path
from .views import metrics_view

urlpatterns = [
    # ...інші маршрути...
    path('metrics', metrics_view, name='metrics'),
]
