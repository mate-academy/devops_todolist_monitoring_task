from prometheus_client import generate_latest, Counter
from django.http import HttpResponse

get_requests_total = Counter('http_get_requests_total', 'Total number of GET requests')
post_requests_total = Counter('http_post_requests_total', 'Total number of POST requests')

def todolist_metrics(request):
  if request.method == 'GET':
    get_requests_total.inc()
  else:
    post_requests_total.inc()

  metrics = generate_latest()
  return HttpResponse(metrics, content_type="text/plain")