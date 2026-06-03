from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


def metrics(request):

    return HttpResponse(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )