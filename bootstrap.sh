#!/usr/bin/env bash
RELEASE_NAME="todoapp-release"
APP_NAMESPACE="todoapp"

kind create cluster --config cluster.yml

kubectl taint nodes -l app=mysql app=mysql:NoSchedule --overwrite

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl rollout status deployment/ingress-nginx-controller \
  --namespace ingress-nginx --timeout=180s

helm dependency build ".infrastructure/helm-charts/todoapp"

helm upgrade --install "$RELEASE_NAME" ".infrastructure/helm-charts/todoapp" \
  --namespace "$APP_NAMESPACE" --create-namespace \