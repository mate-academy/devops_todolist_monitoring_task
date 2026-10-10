from django.test import SimpleTestCase

from todolist.metrics import HTTP_REQUESTS


class MetricsTests(SimpleTestCase):
    def test_metrics_endpoint_returns_prometheus_format(self):
        response = self.client.get("/metrics")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response["Content-Type"].startswith("text/plain")
        )
        self.assertContains(response, "todo_http_requests_total")
        self.assertContains(response, 'method="GET"')

    def test_post_requests_are_counted(self):
        before = HTTP_REQUESTS.labels(method="POST")._value.get()

        self.client.post("/metrics")

        after = HTTP_REQUESTS.labels(method="POST")._value.get()
        self.assertEqual(after, before + 1)