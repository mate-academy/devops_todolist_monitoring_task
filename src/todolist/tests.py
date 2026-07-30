from django.test import SimpleTestCase
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY


class MetricsEndpointTests(SimpleTestCase):
    def test_metrics_endpoint_is_available(self):
        response = self.client.get("/metrics")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            CONTENT_TYPE_LATEST,
        )

    def test_get_request_increments_get_counter(self):
        initial_value = (
            REGISTRY.get_sample_value(
                "todoapp_http_requests_total",
                {"method": "GET"},
            )
            or 0
        )

        self.client.get("/")

        current_value = (
            REGISTRY.get_sample_value(
                "todoapp_http_requests_total",
                {"method": "GET"},
            )
            or 0
        )

        self.assertEqual(current_value, initial_value + 1)

    def test_post_request_increments_post_counter(self):
        initial_value = (
            REGISTRY.get_sample_value(
                "todoapp_http_requests_total",
                {"method": "POST"},
            )
            or 0
        )

        self.client.post("/", {})

        current_value = (
            REGISTRY.get_sample_value(
                "todoapp_http_requests_total",
                {"method": "POST"},
            )
            or 0
        )

        self.assertEqual(current_value, initial_value + 1)

    def test_monitoring_endpoints_do_not_increment_get_counter(self):
        initial_value = REGISTRY.get_sample_value(
            "todoapp_http_requests_total",
            {"method": "GET"},
        )

        for path in ("/metrics", "/api/health", "/api/ready"):
            self.client.get(path)

        current_value = REGISTRY.get_sample_value(
            "todoapp_http_requests_total",
            {"method": "GET"},
        )

        self.assertEqual(current_value, initial_value)

    def test_metrics_endpoint_exposes_get_and_post_counters(self):
        response = self.client.get("/metrics")

        self.assertContains(
            response,
            'todoapp_http_requests_total{method="GET"}',
        )
        self.assertContains(
            response,
            'todoapp_http_requests_total{method="POST"}',
        )
