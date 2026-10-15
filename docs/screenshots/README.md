# Grading Evidence — MediDesk DevOps Capstone

Screenshots/captures below map directly to the evaluation rubric modules.
All evidence was produced by actually running the project — no mockups.

- App stack: FastAPI + PostgreSQL + React/Nginx via `docker compose up --build`
- Kubernetes evidence captured on a local `kind` cluster (`kindest/node:v1.31.0`)
  with `helm upgrade --install medidesk helm/medidesk -f helm/medidesk/values-dev.yaml`
- CI evidence captured from the public repo:
  <https://github.com/rkawasthiii/devops-project/actions>
- Terraform validated locally (`init`/`validate`/`fmt`); `plan`/`apply` require
  AWS credentials on the evaluation machine — see `terraform/README` notes in
  `docs/demo-script.md`.

## Application (Module 1/2)

| File | Shows |
|---|---|
| `m1-dashboard.png` | MediDesk clinic dashboard on `http://localhost:3000` — KPI cards, filters, appointment table, activity feed, live "API live" indicator |
| `m1-booking-modal.png` | Booking modal — POST `/api/appointments` from the UI |
| `m1-swagger.png` | FastAPI `/docs` — GET/POST/PUT/DELETE + stats + ops endpoints |
| `m1-api.png` | curl smoke: `/health`, `/ready`, `/api/appointments/stats`, `/api/appointments`, `/metrics` |

## Testing (Module 3)

| File | Shows |
|---|---|
| `m3-pytest.png` | `pytest` — **17 passed**, `configfile: pytest.ini`, SQLite-isolated test DB (see `backend/conftest.py`) |

## Docker (Module 4)

| File | Shows |
|---|---|
| `m4-compose.png` | `docker compose up --build -d` + `docker compose ps` — postgres healthy, backend+frontend started, ports 8000/3000/5432 |

## CI/CD & Registry (Module 5)

| File | Shows |
|---|---|
| `m5-actions-run.png` | GitHub Actions run `38805866982` — **Success**: Test → Build + Trivy + Push to GHCR (Deploy-to-EKS job conditional, skipped) |
| `m5-actions-list.png` | Workflow runs list — green CI on `main` |
| `m5-ghcr-packages.png` | GitHub → Packages: `medidesk-backend` + `medidesk-frontend` published to `ghcr.io/rkawasthiii` tagged by commit SHA + `latest` |
| `m2-commits.png` | Commit history — meaningful conventional commits |

## Security Scanning (Module 6)

| File | Shows |
|---|---|
| `m6-trivy.png` | `trivy image --severity HIGH,CRITICAL` — backend **0 findings**, frontend **0 findings** (same gate enforced in CI) |

## Terraform / AWS (Module 7)

| File | Shows |
|---|---|
| `m7-terraform.png` | `terraform init -backend=false` (modules + providers resolve), `terraform validate` → `Success! The configuration is valid.`, `terraform fmt -check` clean |

> `terraform plan`/`apply` are intentionally run on the reviewer's AWS account
> during the demo (see `docs/demo-script.md`) — costs stay near zero by using
> `terraform destroy` afterwards. No AWS credentials are stored in this repo.

## Kubernetes & Helm (Module 8)

| File | Shows |
|---|---|
| `m8-helm.png` | `helm lint`, `helm template` (10 resources incl. Deployments, Services, HPA, StatefulSet, Ingress, ServiceMonitor), `kubeconform` → 9 valid / 0 invalid (ServiceMonitor CRD skipped) |
| `m8-kubernetes.png` | Real `kind` cluster: `helm list` (deployed), 5/5 pods Running, ClusterIP services, PVC Bound, Ingress with address, Deployments 2/2 + StatefulSet 1/1, live `curl` through the Ingress |
| `m8-hpa-autoscale.png` | HPA under `scripts/load-test` traffic: `cpu: 261%/70%` → `SuccessfulRescale` events New size 4 → 6, all replicas Ready after burst |
| `m8-app-via-ingress.png` | Full app served through the nginx Ingress at `http://medidesk.local` |

## Monitoring (Module 9)

| File | Shows |
|---|---|
| `m9-metrics.png` | `GET /metrics` — Prometheus exposition incl. `http_requests_total` per handler/method/status |
| `m9-prometheus-targets.png` | Prometheus target `medidesk-backend → http://backend:8000/metrics` **UP** |
| `m9-prometheus-query.png` | PromQL `sum(rate(http_requests_total{job="medidesk-backend"}[1m]))` graph showing the load-test spike |
| `m9-grafana-dashboard.png` | Grafana dashboard "MediDesk — API Overview" (provisioned from `monitoring/dashboard-configmap.yaml`) — req/s, p95 latency, per-handler rates, p50/p95/p99 |

The monitoring screenshots were produced by running Prometheus + Grafana in
Docker against the Compose stack (same scrape job/datasource/dashboard config
as the Helm-based `monitoring/` manifests).
