#!/bin/bash

# Deploy TodoApp with Prometheus Monitoring
# This script deploys the complete monitoring stack

set -e

echo "🚀 Starting TodoApp deployment with Prometheus monitoring..."

# Check if kind is available
if ! command -v kind &> /dev/null; then
    echo "❌ kind is not installed. Please install kind first."
    echo "   Visit: https://kind.sigs.k8s.io/docs/user/quick-start/"
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed. Please install helm first."
    echo "   Visit: https://helm.sh/docs/intro/install/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create kind cluster
echo "📦 Creating kind cluster..."
kind create cluster --config=cluster.yml

# Wait for cluster to be ready
echo "⏳ Waiting for cluster to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=300s

# Add Prometheus Helm repository
echo "📊 Adding Prometheus Helm repository..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
echo "🔧 Installing kube-prometheus-stack..."
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --set admissionWebhooks.enabled=false \
  --set grafana.adminPassword=admin123 \
  --namespace monitoring \
  --create-namespace

# Wait for Prometheus stack to be ready
echo "⏳ Waiting for Prometheus stack to be ready..."
kubectl wait --for=condition=Available deployment --all -n monitoring --timeout=300s

# Deploy MySQL
echo "🗄️ Deploying MySQL..."
kubectl apply -f .infrastructure/mysql/

# Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to be ready..."
kubectl wait --for=condition=Ready pod -l app=mysql -n mysql --timeout=300s

# Deploy TodoApp
echo "📱 Deploying TodoApp..."
kubectl apply -f .infrastructure/app/
kubectl apply -f .infrastructure/security/
kubectl apply -f .infrastructure/ingress/

# Wait for TodoApp to be ready
echo "⏳ Waiting for TodoApp to be ready..."
kubectl wait --for=condition=Available deployment --all -n todoapp --timeout=300s

# Deploy ServiceMonitor
echo "📈 Deploying ServiceMonitor..."
kubectl apply -f .infrastructure/app/servicemonitor.yml

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Access URLs:"
echo "   TodoApp: http://localhost:30007"
echo "   Grafana: http://localhost:3000 (admin/admin123)"
echo "   Prometheus: http://localhost:9090"
echo ""
echo "🔧 Port forwarding commands:"
echo "   kubectl port-forward svc/todoapp-nodeport 30007:80 -n todoapp"
echo "   kubectl port-forward svc/kube-prometheus-stack-grafana 3000:80 -n monitoring"
echo "   kubectl port-forward svc/kube-prometheus-stack-prometheus 9090:9090 -n monitoring"
echo ""
echo "📊 To check metrics:"
echo "   curl http://localhost:30007/metrics"
echo ""
echo "🎉 Happy monitoring!"
