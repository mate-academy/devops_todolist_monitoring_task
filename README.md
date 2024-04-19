# Django ToDo List

In this task you will enhance a todo list web application by adding a /metrics endpoint that returns the number of GET and POST requests in a Prometheus-compatible format.

To do this task, you will need:

- CSS | [Skeleton](http://getskeleton.com/)
- JS  | [jQuery](https://jquery.com/)

## Explore

Try it out by installing the requirements (the following commands work only with Python 3.8 and higher, due to Django 4):

```
pip install -r requirements.txt
```

Create a database schema:

```
python manage.py migrate
```

And then start the server (default is http://localhost:8000):

```
python manage.py runserver
```

Now you can browse the [API](http://localhost:8000/api/) or start on the [landing page](http://localhost:8000/).

## Task
Follow the steps below to complete the task:

1. Fork the repository to your GitHub account.

2. Expose `/metrics` endpoint:
   - Modify the application code to include a `/metrics` endpoint.
   - Ensure it returns the number of GET and POST requests in a Prometheus-compatible format.

3. Add Prometheus library:
   - Include `prometheus_client` in the application's requirements.
   - Ensure it's installed during the Docker build process.

4. Cluster setup:
   - Use `kind` to spin up a cluster from a `cluster.yml` configuration file.

5. Install Prometheus:
   - Install [Prometheus](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) on the cluster using the provided Helm chart.

6. Configure Helm Chart:
   - Update the `values.yaml` file in the `todoapp` Helm chart:
   * Add a new section for the `ServiceMonitor` configuration:
     ```yaml
     serviceMonitor:
         enabled: true
         labels: {}
         interval: 10s
         path: /metrics
         port: http
     ```
   - Create a new file named `servicemonitor.yaml` in the Helm chart's templates directory.
   - Ensure the app's `service.yaml` exposes the metrics port and has the necessary labels for the ServiceMonitor.

7. Apply Helm Chart:
   - Apply the Helm chart to the cluster.
   - Verify that the ServiceMonitor has been created.

8. Verify Prometheus scraping:
   - Check Prometheus dashboard for the target status to ensure it's scraping metrics from the `todoapp`.

9. Create Grafana dashboard:
   - Open the Grafana UI and click on the **+** icon in the sidebar to create a new dashboard.
   - Click **Add new panel** to start configuring your first metric visualization.

10. Visualize total HTTP requests:
    - Set up a panel titled **Total HTTP Requests**.
    - Use the query to visualize the total number of HTTP requests:
        ```
        sum(rate(django_http_requests_total[5m])) by (method)
        ```
    - This query will show the rate of HTTP requests per second, averaged over the past 5 minutes, broken down by method (GET or POST).
    - Choose a visualization type such as Graph, Bar Gauge, or Stat to represent this data.

11. Visualize HTTP requests creation time:
    - Add a panel titled **HTTP Requests Creation Time**.
    - Use the query to visualize the creation time of the requests:
        ```
        django_http_requests_created
        ```
    - This metric represents the time when the HTTP request counters were created or reset, which can be useful for identifying when the application was restarted.
    - Choose a Singlestat or Stat visualization for this metric.

12. Customize panel settings:
    - Adjust panel settings such as axes, legend, and thresholds as desired.
    - Utilize Grafana’s functions for formatting the display.

13. Save and share dashboard:
    - Save the configured dashboard.
    - Export the dashboard JSON for version control and sharing.

14. Submit a PR with your changes for validation on the specified platform.
