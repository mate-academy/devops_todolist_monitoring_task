# TodoApp Kubernetes Deployment with Prometheus Monitoring

This document provides step-by-step instructions for deploying the TodoApp with full Prometheus monitoring stack.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/) installed
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
- [helm](https://helm.sh/docs/intro/install/) installed

## Quick Start

### Option 1: Automated Deployment

Run the deployment script:

```bash
./deploy.sh
```

This script will:
1. Create a kind cluster
2. Install kube-prometheus-stack
3. Deploy MySQL database
4. Deploy TodoApp with monitoring
5. Configure ServiceMonitor for metrics scraping

### Option 2: Manual Deployment

#### 1. Create Kind Cluster

```bash
kind create cluster --config=cluster.yml
```

#### 2. Install Prometheus Stack

```bash
# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --set admissionWebhooks.enabled=false \
  --set grafana.adminPassword=admin123 \
  --namespace monitoring \
  --create-namespace
```

#### 3. Deploy Infrastructure

```bash
# Deploy MySQL
kubectl apply -f .infrastructure/mysql/

# Deploy TodoApp
kubectl apply -f .infrastructure/app/
kubectl apply -f .infrastructure/security/
kubectl apply -f .infrastructure/ingress/

# Deploy ServiceMonitor
kubectl apply -f .infrastructure/app/servicemonitor.yml
```

#### 4. Deploy with Helm Chart

```bash
# Deploy using the custom Helm chart
helm install todoapp ./helm/todoapp/ \
  --namespace todoapp \
  --create-namespace
```

## Accessing the Application

### Port Forwarding

```bash
# TodoApp
kubectl port-forward svc/todoapp-nodeport 30007:80 -n todoapp

# Grafana
kubectl port-forward svc/kube-prometheus-stack-grafana 3000:80 -n monitoring

# Prometheus
kubectl port-forward svc/kube-prometheus-stack-prometheus 9090:9090 -n monitoring
```

### URLs

- **TodoApp**: http://localhost:30007
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090

## Monitoring

### Metrics Endpoint

The application exposes Prometheus metrics at `/metrics`:

```bash
curl http://localhost:30007/metrics
```

### Available Metrics

- `http_requests_total` - Total number of HTTP requests by method and endpoint
- `http_request_duration_seconds` - HTTP request duration histogram
- `http_requests_created` - Timestamp when request counters were created

### Grafana Dashboard

Import the provided dashboard JSON (`grafana-dashboard.json`) into Grafana to visualize:

1. **Total HTTP Requests** - Rate of requests per second
2. **HTTP Requests by Method** - Breakdown by GET/POST
3. **HTTP Request Duration** - 95th and 50th percentile response times
4. **HTTP Requests Creation Time** - When metrics were last reset
5. **Request Rate by Endpoint** - Table view of request rates

### Prometheus Queries

```promql
# Total request rate
sum(rate(http_requests_total[5m]))

# Request rate by method
sum(rate(http_requests_total[5m])) by (method)

# 95th percentile response time
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint, method)
```

## Verification

### Check Pods

```bash
kubectl get pods -n todoapp
kubectl get pods -n monitoring
```

### Check Services

```bash
kubectl get svc -n todoapp
kubectl get svc -n monitoring
```

### Check ServiceMonitor

```bash
kubectl get servicemonitor -n todoapp
```

### Verify Metrics Scraping

1. Open Prometheus UI (http://localhost:9090)
2. Go to Status → Targets
3. Look for `todoapp-servicemonitor` target
4. Verify it's showing as "UP"

## Troubleshooting

### Common Issues

1. **Pods not starting**: Check resource limits and node capacity
2. **Metrics not appearing**: Verify ServiceMonitor configuration and labels
3. **Database connection issues**: Check MySQL pod status and network connectivity

### Useful Commands

```bash
# Check pod logs
kubectl logs -f deployment/todoapp -n todoapp

# Check service endpoints
kubectl get endpoints -n todoapp

# Check Prometheus targets
kubectl port-forward svc/kube-prometheus-stack-prometheus 9090:9090 -n monitoring
# Then visit http://localhost:9090/targets

# Test metrics endpoint
kubectl port-forward svc/todoapp-service 8080:80 -n todoapp
curl http://localhost:8080/metrics
```

## Cleanup

To remove all resources:

```bash
# Delete TodoApp
kubectl delete namespace todoapp

# Delete Prometheus stack
helm uninstall kube-prometheus-stack -n monitoring
kubectl delete namespace monitoring

# Delete MySQL
kubectl delete namespace mysql

# Delete kind cluster
kind delete cluster
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TodoApp       │    │   Prometheus    │    │   Grafana       │
│   (Port 8080)   │───▶│   (Port 9090)   │───▶│   (Port 3000)   │
│   /metrics      │    │   Scraping      │    │   Dashboards    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│   MySQL         │
│   (Port 3306)   │
└─────────────────┘
```

## Features Implemented

✅ `/metrics` endpoint with Prometheus format  
✅ HTTP request tracking (GET/POST counts)  
✅ Request duration histograms  
✅ Kubernetes deployment with Helm  
✅ ServiceMonitor for Prometheus scraping  
✅ Grafana dashboard with visualizations  
✅ Horizontal Pod Autoscaling  
✅ Health and readiness probes  
✅ Ingress configuration  
✅ Secret management  
✅ Resource limits and requests  

## Next Steps

1. Set up alerting rules in Prometheus
2. Configure persistent storage for MySQL
3. Implement SSL/TLS termination
4. Set up log aggregation with ELK stack
5. Implement distributed tracing
