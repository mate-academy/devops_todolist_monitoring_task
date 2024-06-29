from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from api.serializers import TodoListSerializer, TodoSerializer, UserSerializer
from lists.models import Todo, TodoList

from django.http import HttpResponse
from django.utils import timezone
from prometheus_client import Counter, generate_latest

import time

startup_time = timezone.now()

get_counter = Counter('http_requests_get_total', 'Total number of GET requests')
post_counter = Counter('http_requests_post_total', 'Total number of POST requests')

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `creator` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # If the object doesn't have a creator (i.e. anon) allow all methods.
        if not obj.creator:
            return True

        # Instance must have an attribute named `creator`.
        return obj.creator == request.user


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class TodoListViewSet(viewsets.ModelViewSet):

    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)


class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)

# Health Check View
def health(request):
    return HttpResponse("Health OK", content_type="text/plain")

# Readiness Check View
def ready(request):
    # Calculate elapsed time since startup
    elapsed_time = timezone.now() - startup_time
    if elapsed_time.total_seconds() < 30:
        # Return HTTP 500 for the first 30 seconds after startup
        return HttpResponse("Service not ready", status=500, content_type="text/plain")
    else:
        # After 30 seconds, return HTTP 200
        return HttpResponse("Readiness OK", content_type="text/plain")
def metrics(request):
    if request.method == 'GET':
        get_counter.inc()
    elif request.method == 'POST':
        post_counter.inc()

    return HttpResponse(generate_latest(), content_type='text/plain; version=0.0.4')
