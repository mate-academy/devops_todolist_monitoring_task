#!/bin/bash
set -euo pipefail

# Create the kind cluster and wait for it to come up
kind create cluster --config cluster.yml --wait 90s

kubectl taint nodes -l app=mysql app=mysql:NoSchedule

kubectl apply -f metrics.yml

kubectl wait --namespace kube-system \
  --for=condition=available deployment/metrics-server \
  --timeout=90s

# Install Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Force controller onto the node with the hostPort mapping
kubectl patch deployment ingress-nginx-controller -n ingress-nginx --type='json' \
  -p='[{"op":"add","path":"/spec/template/spec/nodeSelector/ingress-ready","value":"true"}]'

kubectl wait --namespace ingress-nginx \
  --for=condition=complete job/ingress-nginx-admission-patch \
  --timeout=120s

kubectl wait --namespace ingress-nginx \
  --for=condition=Ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Prometheus stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

rm -rf ./kube-prometheus-stack
helm pull prometheus-community/kube-prometheus-stack --version 87.15.1 --untar
helm upgrade --install kube-prometheus-stack ./kube-prometheus-stack -n monitoring --wait

helm upgrade --install todoapp ./.infrastructure/helm-chart/todoapp --wait