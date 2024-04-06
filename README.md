# Django ToDo list

This is a todo list web application with basic features of most web apps, i.e., accounts/login, API, and interactive UI. To do this task, you will need:

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

1. Fork this repository.
2. Modify the application code to expose `/metrics` endpoint that returns number of GET and POST requests in a Prometheus-compatible format.
3. Add the necessary library (`prometheus_client`) to your application's requirements and ensure it is installed during the Docker build process.
4. Use `kind` to spin up a cluster from a `cluster.yml` configuration file.
5. Install [Prometheus](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) on the cluster.
6. Configure your `todoapp` Helm chart to enable Prometheus to scrape metrics
    Update `values.yaml`:

    * Add a new section for the `ServiceMonitor` configuration:

        ```yaml
        serviceMonitor:
            enabled: true
            labels: {}
            interval: 10s
            path: /metrics
            port: http
        ``` 
    
    * In the Helm chart's templates directory, create a new file named `servicemonitor.yaml`
    * Make sure your app's `service.yaml` exposes the metrics port and has the necessary labels for the ServiceMonitor to select
7. Apply the Helm chart to your cluster and check that the ServiceMonitor has been created.
8. Ensure that Prometheus is scraping metrics from the `todoapp`: check the Prometheus dashboard for the target status.
9. Create a New Grafana Dashboard:
    * Open the Grafana UI and click on the "+" icon in the sidebar to create a new dashboard.
    * Click "Add new panel" to start configuring your first metric visualization.

10. Visualize Total HTTP Requests:
    * Set the Panel Title to "Total HTTP Requests".
    * In the query field, enter the Prometheus query to visualize the total number of HTTP requests. Use the metric             `django_http_requests_total`:
        ```
        sum(rate(django_http_requests_total[5m])) by (method)
        ```
    * This query will show the rate of HTTP requests per second, averaged over the past 5 minutes, broken down by method (GET or POST).
    * Choose a visualization type such as Graph, Bar Gauge, or Stat to represent this data.

11. Visualize HTTP Requests Creation Time:
    * Add another panel to the dashboard.
    * Set the Panel Title to "HTTP Requests Creation Time".
    * In the query field, use the `django_http_requests_created` metric to visualize the creation time of the requests:
        ```
        django_http_requests_created
        ```
    * This metric represents the time when the HTTP request counters were created or reset, which can be useful for identifying when the application was restarted.
    * Choose a Singlestat or Stat visualization for this metric.

12. Tweak Panel Settings:
    * Customize the panel settings such as axes, legend, and thresholds according to your preference.
    * Use Grafana’s built-in functions to format the display, such as setting the unit to "requests per second" for the total requests panel.

13. Save and Share the Dashboard:
    * After configuring the panels, save your dashboard.
    * Export the dashboard JSON from the dashboard settings menu for version control and sharing.
14. Create PR with your changes and attach it for validation on a platform.
