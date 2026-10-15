"""Operational endpoint tests: health, readiness, metrics."""


def test_root_returns_service_info(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["service"] == "medidesk-api"
    assert "version" in body


def test_health_is_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_ready_checks_database(client):
    resp = client.get("/ready")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ready"}


def test_metrics_exposes_prometheus_format(client):
    client.get("/health")  # generate at least one observation
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "http_requests_total" in resp.text
