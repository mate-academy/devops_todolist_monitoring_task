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

2. Create a new `/metrics` endpoint (not `api/metrics`):
   - Modify the application code to include a `/metrics` endpoint.
   - Ensure it returns the number of GET and POST requests in a Prometheus-compatible format.

3. Add Prometheus library:
   - Include `prometheus_client` in the application's requirements.
   - Ensure it's installed during the Docker build process.

4. Cluster setup:
   - Use `kind` to spin up a cluster from a `cluster.yml` configuration file.

5. Pull the kube-prometheus-stack:
   - [Prometheus](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
   ```bash
   helm pull prometheus-community/kube-prometheus-stack --version <version_number> --untar
   ```

6. Install the kube-prometheus-stack Helm chart:
   ```bash
   helm install kube-prometheus-stack ./kube-prometheus-stack
   ```
    * **Note**: If you encounter issues deploying on Ubuntu, particularly related to the admission controller, find the `admissionWebhooks` section in the `values.yaml` and set:
   ```yaml
   admissionWebhooks:
     enabled: false
   ```

7. Modify the `values.yaml` file in the `todoapp` Helm chart:
   ```yaml
      serviceMonitor:
        enabled: true
        labels: {}
        interval: 10s
        path: /metrics
        port: http
    ```

8. Configure your `todoapp` Helm chart:
   - In the Helm chart's templates directory, create a new file named `servicemonitor.yaml` with the necessary configuration.
   - Ensure your app's `service.yaml` exposes the metrics port and has the necessary labels for the ServiceMonitor to select.
   - Perform port forwarding to your application service to expose the metrics endpoint:
      ```bash
      kubectl port-forward svc/<your-service-name> 8080:<app-port>
      ```
9. Apply Helm Chart:
   - Apply the Helm chart to the cluster.
   - Verify that the ServiceMonitor has been created.

10. Verify Prometheus scraping:
   - Check Prometheus dashboard for the target status to ensure it's scraping metrics from the `todoapp`.

11. Create Grafana dashboard:
   - Open the Grafana UI and click on the **+** icon in the sidebar to create a new dashboard.
   - Click **Add new panel** to start configuring your first metric visualization.

12. Visualize total HTTP requests:
    - Set up a panel titled **Total HTTP Requests**.
    - Use the query to visualize the total number of HTTP requests:
        ```
        sum(rate(<your_custom_metric>[5m])) by (method)
        ```
    - This query will show the rate of HTTP requests per second, averaged over the past 5 minutes, broken down by method (GET or POST).
    - Choose a visualization type such as Graph, Bar Gauge, or Stat to represent this data.

13. Visualize HTTP requests creation time:
    - Add a panel titled **HTTP Requests Creation Time**.
    - Use the query to visualize the creation time of the requests:
        ```
        <your_custom_metric>
        ```
    - This metric represents the time when the HTTP request counters were created or reset, which can be useful for identifying when the application was restarted.
    - Choose a Singlestat or Stat visualization for this metric.

14. Customize panel settings:
    - Adjust panel settings such as axes, legend, and thresholds as desired.
    - Utilize Grafana’s functions for formatting the display.

14. Submit a PR with your changes and attach screenshots of your Grafana dashboard for validation on the specified platform.

## Implementation Status

✅ **Completed Implementation:**

### 1. Prometheus Metrics Integration
- Added `prometheus_client==0.19.0` to requirements.txt
- Created `/metrics` endpoint that returns Prometheus-compatible format
- Implemented middleware to track HTTP requests (GET and POST counts)
- Added request duration histograms for performance monitoring

### 2. Kubernetes Deployment
- Created complete Helm chart for TodoApp deployment
- Configured ServiceMonitor for Prometheus scraping
- Set up horizontal pod autoscaling (HPA)
- Implemented health and readiness probes
- Added proper resource limits and requests

### 3. Monitoring Stack
- Created Grafana dashboard with comprehensive visualizations
- Configured Prometheus metrics scraping
- Set up proper service discovery and labeling
- Added monitoring for request rates, durations, and endpoints

### 4. Infrastructure as Code
- Complete Kubernetes manifests in `.infrastructure/` directory
- Helm chart with configurable values
- Automated deployment scripts
- Comprehensive documentation and testing tools

## Quick Start

### Prerequisites
- Docker installed and running
- kind, kubectl, and helm installed

### Deploy Everything
```bash
# Clone the repository
git clone <your-repo-url>
cd devops_todolist_monitoring_task

# Run automated deployment
./deploy.sh
```

### Access the Application
- **TodoApp**: http://localhost:30007
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090

### Test Metrics
```bash
# Test local development
./test-metrics.sh local

# Test Kubernetes deployment
./test-metrics.sh k8s
```

## Files Added/Modified

### New Files
- `src/todolist/metrics.py` - Prometheus metrics endpoint
- `src/todolist/middleware.py` - HTTP request tracking middleware
- `helm/todoapp/` - Complete Helm chart
- `grafana-dashboard.json` - Grafana dashboard configuration
- `deploy.sh` - Automated deployment script
- `test-metrics.sh` - Metrics testing script
- `DEPLOYMENT.md` - Comprehensive deployment guide

### Modified Files
- `src/requirements.txt` - Added prometheus_client
- `src/todolist/urls.py` - Added /metrics endpoint
- `src/todolist/settings.py` - Added Prometheus middleware
- `.infrastructure/app/clusterIp.yml` - Added metrics port
- `.infrastructure/security/rbac.yml` - Fixed namespace

## Metrics Available

The application now exposes the following Prometheus metrics:

- `http_requests_total` - Total HTTP requests by method and endpoint
- `http_request_duration_seconds` - Request duration histogram
- `http_requests_created` - Timestamp when counters were created

## Grafana Dashboard

The included dashboard provides:
1. **Total HTTP Requests** - Rate of requests per second
2. **HTTP Requests by Method** - Breakdown by GET/POST
3. **HTTP Request Duration** - 95th and 50th percentile response times
4. **HTTP Requests Creation Time** - When metrics were last reset
5. **Request Rate by Endpoint** - Table view of request rates

## Screenshots

*Note: Screenshots would be added here showing:*
- Grafana dashboard with metrics visualizations
- Prometheus targets showing successful scraping
- TodoApp running with /metrics endpoint accessible