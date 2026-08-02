from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from api.serializers import TodoListSerializer, TodoSerializer, UserSerializer
from lists.models import Todo, TodoList

from django.http import HttpResponse
from django.utils import timezone

startup_time = timezone.now()

REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'view']
)

class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not obj.creator:
            return True
        return obj.creator == request.user

class InstrumentedViewSet(viewsets.ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        # Використовуємо назву класу для мітки 'view'
        REQUEST_COUNT.labels(
            method=request.method, 
            view=self.__class__.__name__
        ).inc()
        return super().dispatch(request, *args, **kwargs)

class UserViewSet(InstrumentedViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class TodoListViewSet(InstrumentedViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)

class TodoViewSet(InstrumentedViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)

def health(request):
    REQUEST_COUNT.labels(method='GET', view='health').inc()
    return HttpResponse("Health OK", content_type="text/plain")

def ready(request):
    REQUEST_COUNT.labels(method='GET', view='ready').inc()
    elapsed_time = timezone.now() - startup_time
    if elapsed_time.total_seconds() < 30:
        return HttpResponse("Service not ready", status=500, content_type="text/plain")
    return HttpResponse("Readiness OK", content_type="text/plain")

def metrics(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)