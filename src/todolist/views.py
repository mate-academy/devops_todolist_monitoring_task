from django.http import HttpResponse

from todolist.metrics import get_metrics_response


def metrics_view(request):
    metrics_body, content_type = get_metrics_response()
    return HttpResponse(metrics_body, content_type=content_type)
