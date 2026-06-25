#!/bin/bash


# Install Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

for node in $(kubectl get nodes -l app=mysql -o name); do
  kubectl taint "$node" app=mysql:NoSchedule
done

# Install prometheus from web
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --version 87.2.0 --namespace monitoring --create-namespace

# Install  todoapp
helm install todoapp .infrastructure/helm-chart/todoapp
