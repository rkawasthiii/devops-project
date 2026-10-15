# Troubleshooting lab

Two deliberately broken manifests used to practice the standard Kubernetes
debugging workflow. Both live in the `medidesk` namespace and do not affect
the healthy deployment.

## Exercise 1 — ImagePullBackOff

```bash
kubectl apply -f troubleshooting/broken-image.yaml
kubectl get pods -n medidesk -w
kubectl describe pod -l app=medidesk-backend-broken -n medidesk
kubectl get events -n medidesk --sort-by=.lastTimestamp
```

The Pod sits in `ImagePullBackOff` because the tag `does-not-exist` was never
pushed to GHCR. The fix is to point the Deployment at a real tag (a commit
SHA published by the pipeline):

```bash
kubectl set image deployment/medidesk-backend-broken \
  backend=ghcr.io/rkawasthiii/medidesk-backend:latest -n medidesk
kubectl rollout status deployment/medidesk-backend-broken -n medidesk
```

## Exercise 2 — Service selects nothing

```bash
kubectl apply -f troubleshooting/broken-service.yaml
kubectl get svc medidesk-backend-unreachable -n medidesk
kubectl get endpoints medidesk-backend-unreachable -n medidesk   # empty
kubectl get pods -n medidesk --show-labels
```

The Service's selector asks for `app.kubernetes.io/component: backendd` —
a label no Pod carries — so its endpoint list stays empty. Compare the labels
on the real backend Pods, then correct the selector to `backend` and
re-apply; the endpoints populate immediately.

## Cleanup

```bash
kubectl delete -f troubleshooting/broken-image.yaml
kubectl delete -f troubleshooting/broken-service.yaml
```
