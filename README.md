# MediDesk — Clinic Appointment Management Platform

**DevOps Final Capstone Project**

| | |
|---|---|
| **Student** | Radhey Krishna Awasthi |
| **Roll No.** | 10242 |
| **Email** | radhey.24bcs10242@sst.scaler.com |

MediDesk is a SaaS-style operations dashboard for a multi-speciality clinic.
Reception staff book appointments, track today's schedule, watch department
load and manage the visit lifecycle (scheduled → completed / cancelled) from
one screen. Underneath the UI it is a complete DevOps reference
implementation: the application is tested, containerised, scanned, published
to a container registry, and deployed onto Kubernetes infrastructure that is
itself provisioned from code.

---

## Architecture

```text
Developer ──▶ Git/GitHub ──▶ GitHub Actions
                              │  pytest (quality gate)
                              │  frontend production build
                              │  docker build × 2
                              │  Trivy scan (HIGH/CRITICAL gate)
                              └─▶ GHCR  (tagged with the commit SHA)
                                        │
Terraform ──▶ AWS VPC + EKS ◀───────────┘
                    │
                  Helm ──▶ Kubernetes namespace "medidesk"
                            ├── frontend ×2  (React served by Nginx)
                            ├── backend  ×2  (FastAPI + Uvicorn)  ◀─ HPA
                            ├── postgres ×1  (StatefulSet + PVC)
                            ├── Ingress  (/api,/docs,/metrics → backend, / → frontend)
                            └── ServiceMonitor ──▶ Prometheus ──▶ Grafana
```

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite, served by unprivileged Nginx |
| Backend | Python 3.12 · FastAPI · SQLAlchemy 2 · Alembic · psycopg 3 |
| Database | PostgreSQL 16 |
| Tests | Pytest (in-memory SQLite via dependency override) |
| Containers | Docker, multi-stage builds, non-root images |
| CI/CD | GitHub Actions → GHCR · Trivy gate |
| Infra | Terraform (AWS VPC + EKS) |
| Orchestration | Kubernetes + Helm · Ingress (NGINX) · HPA |
| Observability | Prometheus + Grafana |

---

## Repository layout

```text
├── backend/            FastAPI app, Alembic migrations, pytest suite, Dockerfile
├── frontend/           React dashboard, Nginx template, multi-stage Dockerfile
├── docker-compose.yml  one-command local stack (postgres + backend + frontend)
├── .github/workflows/  CI/CD pipeline
├── terraform/          AWS VPC + EKS infrastructure as code
├── helm/medidesk/      Helm chart (deployments, services, ingress, HPA, postgres)
├── k8s/                bootstrap namespace manifest
├── monitoring/         Prometheus & Grafana Helm values + dashboard ConfigMap
├── troubleshooting/    deliberately-broken manifests + walkthrough
├── scripts/            HPA load generator (bash + PowerShell)
└── docs/               presentation demo script
```

---

## 1. Run it locally — fastest path

Requires Docker + Docker Compose.

```bash
docker compose up --build
```

Then open:

```text
http://localhost:3000          → MediDesk dashboard
http://localhost:8000/docs     → FastAPI Swagger UI
http://localhost:8000/health   → liveness
http://localhost:8000/metrics  → Prometheus metrics
```

The backend container waits for PostgreSQL, runs `alembic upgrade head`,
seeds a realistic demo schedule when the table is empty, then starts Uvicorn.
Tear down with `docker compose down` (add `-v` to drop the data volume).

## 2. Develop without containers

```bash
# backend (needs a reachable PostgreSQL)
cd backend
python -m venv .venv && .venv\Scripts\activate        # bash: source .venv/bin/activate
pip install -r requirements.txt
set DATABASE_URL=postgresql+psycopg://medidesk:medidesk@localhost:5432/medidesk
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# frontend (Vite dev server proxies /api → localhost:8000)
cd frontend
npm install
npm run dev      # http://localhost:5173
```

## 3. API surface

```text
GET    /                     service info
GET    /health               liveness (cheap, no dependencies)
GET    /ready                readiness (verifies the database)
GET    /metrics              Prometheus metrics

GET    /api/appointments     list (filters: status, department, doctor, search)
GET    /api/appointments/stats
GET    /api/appointments/{id}
POST   /api/appointments
PUT    /api/appointments/{id}
DELETE /api/appointments/{id}
```

`/health` answers "is the process alive" while `/ready` answers "can it serve
traffic" — Kubernetes uses them for the liveness and readiness probes.

## 4. Tests

```bash
cd backend
pytest -v
```

Sixteen tests cover CRUD, filters, validation errors, stats aggregation and
the operational endpoints. They run against an **in-memory SQLite** engine via
FastAPI dependency override — the production database is never touched. In CI
this suite is the first quality gate: images are only built and pushed when
every test is green.

## 5. CI/CD pipeline

`.github/workflows/ci.yml` runs three stages on every push to `main`:

1. **Test** — `pytest` plus a real production `npm run build`.
2. **Build + Scan + Push** — both images are built, scanned with Trivy
   (fails on HIGH/CRITICAL, ignoring unfixable advisories) and pushed to GHCR
   tagged with the **commit SHA** (plus `latest`). SHA tagging means any
   running image can be traced back to the exact commit that produced it.
3. **Deploy** — gated behind the `DEPLOY_TO_EKS` repository variable; when
   enabled it configures AWS credentials, updates kubeconfig for the EKS
   cluster and runs `helm upgrade --install` with the new SHA tags.

Published images:

```text
ghcr.io/rkawasthiii/medidesk-backend:<sha>
ghcr.io/rkawasthiii/medidesk-frontend:<sha>
```

### What Trivy scans

The pipeline builds each image first, then Trivy inspects the OS packages and
the application libraries inside both images and fails the job if it finds a
HIGH or CRITICAL vulnerability with a published fix — so a known-vulnerable
image never reaches the registry. It is one control among several layers
(SAST, dependency and secret scanning, runtime security), not a guarantee on
its own.

## 6. Infrastructure — Terraform

`terraform/` provisions everything the cluster needs on AWS (default region
`ap-south-1`): a VPC with **two public and two private subnets** across two
AZs, a NAT gateway, and an **EKS cluster with a managed node group** in the
private subnets. The applying identity is granted cluster-admin automatically.

```bash
cd terraform
terraform init
terraform plan
terraform apply          # creates VPC + EKS (~15–20 min)
terraform output configure_kubectl   # run the printed aws eks command
# ... demo / grade ...
terraform destroy        # IMPORTANT: tears everything down
```

Copy `terraform.tfvars.example` → `terraform.tfvars` to customise. AWS
credentials come from the environment or an AWS CLI profile — nothing
sensitive is committed.

## 7. Kubernetes + Helm

Works on any cluster (kind/minikube locally, or the EKS cluster above).

```bash
kubectl apply -f k8s/namespace.yaml

# optional: NGINX ingress controller + metrics-server (needed for Ingress/HPA)
helm upgrade --install medidesk ./helm/medidesk \
  -n medidesk -f helm/medidesk/values-dev.yaml
```

What the chart installs:

| Resource | Detail |
|---|---|
| `Deployment` ×2 | backend & frontend, **2 replicas each**, non-root, probes, resource requests |
| `Service` ×3 | ClusterIP for backend + frontend, headless for postgres |
| `StatefulSet` | PostgreSQL with a PersistentVolumeClaim |
| `Secret` | database credentials consumed via `secretKeyRef` |
| `Ingress` | `/api`, `/docs`, `/health`, `/metrics`… → backend · `/` → frontend |
| `HPA` | autoscaling/v2, CPU 70%, 2→6 backend replicas |
| `ServiceMonitor` | optional Prometheus Operator integration |

Quick check without an ingress controller:

```bash
kubectl port-forward svc/medidesk-frontend 3000:80 -n medidesk   # http://localhost:3000
kubectl get pods -n medidesk    # all Running
helm list -n medidesk
```

For the ingress host `medidesk.local`, add `127.0.0.1 medidesk.local` to the
hosts file (`C:\Windows\System32\drivers\etc\hosts` on Windows).

### Autoscaling demo

```bash
kubectl port-forward svc/medidesk-backend 8000:80 -n medidesk &
./scripts/load-test.sh http://localhost:8000 180      # or .ps1 on Windows
kubectl get hpa -n medidesk -w
```

## 8. Monitoring — Prometheus + Grafana

See `monitoring/README.md`. In short: the backend exports
`/metrics`; `monitoring/prometheus-values.yaml` installs Prometheus with a
dedicated scrape job for the backend Service, and
`monitoring/grafana-values.yaml` installs Grafana pre-wired with the
Prometheus datasource and a sidecar that auto-loads the shipped
**MediDesk — API Overview** dashboard (request rate, latency percentiles,
error rate, in-flight requests).

## 9. Troubleshooting lab

`troubleshooting/` ships two deliberately broken manifests — a bad image tag
(`ImagePullBackOff`) and a Service whose selector matches nothing (empty
endpoints) — with a written walkthrough of `describe`, `events`,
`get endpoints` and `--show-labels` used to isolate each fault.

## 10. Presentation demo flow

`docs/demo-script.md` is a minute-by-minute walkthrough: commit → pipeline →
Trivy → GHCR → Helm release → Ingress → HPA → Grafana → break-and-fix.

---

*Submitted for the Scaler DevOps Final Capstone — Session 21.*
