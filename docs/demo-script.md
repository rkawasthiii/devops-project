# Presentation demo script

A walkthrough that shows the whole path from a code change to a monitored
Kubernetes deployment — the same order the course rubric follows.

## 1. The application

- Open `http://localhost:3000` (compose) or the ingress host.
- Point out the KPI cards, status filters, department search and the
  activity feed; book one appointment through the modal.
- Open `/docs` for Swagger and create/complete/cancel a visit there.

## 2. Tests

- `cd backend && pytest -v` — explain the SQLite override in `conftest.py`
  and that CI runs this gate before any image is built.

## 3. Git + pipeline

- Make a visible change (e.g. rename a KPI label in `KpiCards.jsx`),
  `git add -p`, commit with a meaningful message, push to `main`.
- Open **Actions**: watch `test → build-scan-push`. Show the Trivy step
  output and explain the HIGH/CRITICAL gate and `ignore-unfixed`.
- Show GHCR packages with the new commit-SHA tag.

## 4. Infrastructure

- Walk `terraform/` — VPC module, public/private subnets, NAT, EKS managed
  node group — then `terraform plan` output and the AWS console.
- Show `outputs.tf`'s `configure_kubectl` command.

## 5. Kubernetes + Helm

- `helm list -n medidesk`, `kubectl get pods,svc,hpa -n medidesk`.
- Explain: Deployments (2 replicas), headless postgres StatefulSet+PVC,
  Secret → `DATABASE_URL` env composition, probes, resource requests.
- Open the app through the Ingress host; show `/api` and `/docs` routing.

## 6. Autoscaling

- Run `scripts/load-test.sh` against the port-forwarded backend and watch
  `kubectl get hpa -n medidesk -w` scale 2→4+ pods; scale-down afterwards.

## 7. Observability

- `curl` `/metrics` raw output; Prometheus **Status → Targets** shows
  `medidesk-backend` UP; Grafana dashboard fills with live request data.

## 8. Failure drill

- Apply `troubleshooting/broken-image.yaml`, observe `ImagePullBackOff`,
  fix with `kubectl set image`; then `broken-service.yaml`, show empty
  endpoints, correct the selector, verify endpoints populate.

## 9. Wrap

- `terraform destroy` (if AWS was used), `helm uninstall`,
  `docker compose down -v` — leave nothing running.
