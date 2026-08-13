from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse
from metric import (
    request_count, request_duration, 
    active_tasks, errors
)

def metrics(request):
    """Prometheus metrics endpoint"""
    return HttpResponse(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST
    )

def get_task_count():
    """Оновлюємо лічильник активних завдань"""
    from lists.models import Task
    count = Task.objects.filter(completed=False).count()
    active_tasks.set(count)
    return count