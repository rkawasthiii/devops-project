# Monitoring — Prometheus + Grafana

The backend already exposes Prometheus-formatted metrics at `/metrics`
(via `prometheus-fastapi-instrumentator`). This directory contains the Helm
values used to stand the stack up and a pre-built Grafana dashboard.

## Install (two releases, one namespace)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

kubectl create namespace monitoring
helm install prometheus prometheus-community/prometheus -n monitoring -f monitoring/prometheus-values.yaml
helm install grafana grafana/grafana -n monitoring -f monitoring/grafana-values.yaml

# load the MediDesk dashboard (picked up by Grafana's sidecar)
kubectl apply -f monitoring/dashboard-configmap.yaml
```

`prometheus-values.yaml` adds a `medidesk-backend` scrape job that discovers
the backend Pods through Kubernetes endpoints and keeps only the
`*-backend` Service in the `medidesk` namespace — check
**Status → Targets** in the Prometheus UI to see it `UP`.

`grafana-values.yaml` provisions a default Prometheus datasource and a
dashboard sidecar watching for ConfigMaps labelled `grafana_dashboard=1`.
Open the dashboard under **Dashboards → MediDesk → MediDesk — API Overview**.

## Access the UIs (local cluster)

```bash
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring   # http://localhost:9090
kubectl port-forward svc/grafana 3001:80 -n monitoring             # http://localhost:3001
```

Grafana login: `admin` / `medidesk123` (demo values — change for anything real).

## Alternative: kube-prometheus-stack

The chart also ships a `ServiceMonitor` template. If you prefer the
`kube-prometheus-stack` umbrella chart (Prometheus + Grafana + operator in
one release), install it and then redeploy MediDesk with
`--set serviceMonitor.enabled=true` so the operator registers the scrape
target.
