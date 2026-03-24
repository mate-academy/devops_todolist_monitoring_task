from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from todolist.metrics import HTTP_REQUESTS_TOTAL
from todolist.middleware import PrometheusMetricsMiddleware
from todolist.views import metrics


class MetricsTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_metrics_endpoint_exposes_counter(self):
        response = metrics(self.factory.get("/metrics"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("todoapp_http_requests_total", response.content.decode())

    def test_middleware_counts_get_and_post(self):
        get_before = HTTP_REQUESTS_TOTAL.labels(method="GET")._value.get()
        post_before = HTTP_REQUESTS_TOTAL.labels(method="POST")._value.get()

        middleware = PrometheusMetricsMiddleware(lambda request: HttpResponse("ok"))
        middleware(self.factory.get("/"))
        middleware(self.factory.post("/api/todos/"))
        middleware(self.factory.put("/api/todos/"))
        middleware(self.factory.get("/metrics"))

        self.assertEqual(
            HTTP_REQUESTS_TOTAL.labels(method="GET")._value.get(), get_before + 1
        )
        self.assertEqual(
            HTTP_REQUESTS_TOTAL.labels(method="POST")._value.get(), post_before + 1
        )
