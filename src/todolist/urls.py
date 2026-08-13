from django.contrib import admin
from django.urls import path, include
from todolist.metrics import metrics

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lists.urls')),
    path('accounts/', include('accounts.urls')),
    path('metrics', metrics, name='metrics'),
]