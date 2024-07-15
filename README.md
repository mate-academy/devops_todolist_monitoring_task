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


---

# SOLUTION

### Edit the docker image

1. insert prometheus library in requirements.txt
2. in order to scrape GET/POST requests counter from entire app

    we needed to: 

    * create new middleware `metrics_middleware.py` and insert it in the `todolist.settings.MIDDLEWARE`
    * create new view `metrics` in `api.views`
    * add new endpoint in `todolist.urls`
3. build new docker image
4. tag and push to docker hub

### Create Prometheus helm chart

use `prometheus-community/kube-prometheus-stack`

1. add helm repo with `prometheus-community/kube-prometheus-stack`
2. update helm repo
3. install prometheus stack with default settings

### Create the app helm chart

1. Create the todoapp helm chart
2. Create the mysql subchart
3. add mysql dependancy in todoapp/chart.yaml
4. clean both values.yml files as template value referances creation is not our task
5. copy manifest in relative templates directories
6. change the image in deployment.yml for the one pushed to the docker hub
7. create servicemonitor.yml file to set metrics scraping

    1. Отримаємо `serviceMonitorSelector`

        виведемо конфігурацію Prometheus

        ```sh
        kubectl get prometheuses.monitoring.coreos.com -o yaml
        ```

        -> `release: prometheus`  (use it as label) in serviceMonitor
    2. Add directives for label, endpoint, namespace
8. modify existing ClusterIP service (since it is responsible for inter-cluster communication) to set proper link of Prometheus_ServiceMonitor to the App pods

    add matching label and port name as stated in Servicemonitor
9. install helm chart
10. apply the ingress controller in order to have straight-forward access to our app via localhost

     ```sh
     kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
     ```

### Verify all works / Create Grafana dashboard

1. enter the app and create few lists to make some POST requests
2. verify the metrics endpoint `localhost/metrics`

    get names for the metrics we need to apply in grafana
3. port-forward Prometheus & Grafana
4. Verify the presence of the todoapp pods as UP targets
5. create Grafana dashboard