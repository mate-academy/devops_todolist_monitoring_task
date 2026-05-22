# TodoApp Helm Chart

This Helm chart deploys the Django ToDo List application with Prometheus monitoring integration.

## Features

- Django ToDo List application deployment
- Service configuration with metrics endpoint
- ServiceMonitor for Prometheus integration
- Configurable resource limits and requests
- Environment variable configuration

## Prerequisites

- Kubernetes cluster
- Helm 3.x
- kube-prometheus-stack installed (for ServiceMonitor support)

## Installation

```bash
helm install todoapp .infrastructure/todoapp
```

Or with custom values:

```bash
helm install todoapp .infrastructure/todoapp -f custom-values.yaml
```

## Configuration

The following table lists the configurable parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Image repository | `todoapp` |
| `image.tag` | Image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `8080` |
| `service.targetPort` | Container port | `8080` |
| `serviceMonitor.enabled` | Enable ServiceMonitor | `true` |
| `serviceMonitor.interval` | Scraping interval | `10s` |
| `serviceMonitor.path` | Metrics path | `/metrics` |

## Monitoring

The chart includes a ServiceMonitor resource that automatically configures Prometheus to scrape metrics from the `/metrics` endpoint.

### Prometheus Metrics

The application exposes the following metrics:

- `http_get_requests_total` - Total number of GET requests
- `http_post_requests_total` - Total number of POST requests

### Grafana Dashboard

Use the following queries in Grafana:

1. **Total HTTP Requests**:
   ```
   sum(rate(http_get_requests_total[5m])) by (method) + sum(rate(http_post_requests_total[5m])) by (method)
   ```

2. **HTTP Request Rate by Method**:
   ```
   rate(http_get_requests_total[5m])
   rate(http_post_requests_total[5m])
   ```

## Port Forwarding

To access the application locally:

```bash
kubectl port-forward svc/todoapp-service 8080:8080
```

Then access:
- Application: http://localhost:8080
- Metrics: http://localhost:8080/metrics

## Uninstallation

```bash
helm uninstall todoapp
```
