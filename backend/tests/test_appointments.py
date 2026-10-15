"""CRUD and statistics tests for the appointments API."""

from datetime import datetime, timedelta


def _create(client, **overrides):
    payload = {
        "patient_name": "Test Patient",
        "doctor_name": "Dr. Test",
        "department": "General Medicine",
        "scheduled_at": (datetime.now() + timedelta(days=1)).isoformat(),
    }
    payload.update(overrides)
    return client.post("/api/appointments", json=payload)


def test_create_appointment(client, sample_appointment):
    resp = client.post("/api/appointments", json=sample_appointment)
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] > 0
    assert body["patient_name"] == "Test Patient"
    assert body["status"] == "scheduled"


def test_create_appointment_requires_patient_name(client, sample_appointment):
    del sample_appointment["patient_name"]
    resp = client.post("/api/appointments", json=sample_appointment)
    assert resp.status_code == 422


def test_create_appointment_rejects_bad_status(client, sample_appointment):
    sample_appointment["status"] = "not-a-status"
    resp = client.post("/api/appointments", json=sample_appointment)
    assert resp.status_code == 422


def test_list_appointments_empty(client):
    resp = client.get("/api/appointments")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_appointments_after_create(client):
    _create(client)
    _create(client, patient_name="Second Patient")
    resp = client.get("/api/appointments")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_appointment_by_id(client):
    created = _create(client).json()
    resp = client.get(f"/api/appointments/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_appointment_not_found(client):
    assert client.get("/api/appointments/9999").status_code == 404


def test_update_appointment_status(client):
    created = _create(client).json()
    resp = client.put(
        f"/api/appointments/{created['id']}", json={"status": "completed"}
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


def test_update_appointment_not_found(client):
    resp = client.put("/api/appointments/9999", json={"status": "completed"})
    assert resp.status_code == 404


def test_delete_appointment(client):
    created = _create(client).json()
    assert client.delete(f"/api/appointments/{created['id']}").status_code == 204
    assert client.get(f"/api/appointments/{created['id']}").status_code == 404


def test_filter_by_status(client):
    _create(client, patient_name="Scheduled One")
    second = _create(client, patient_name="Done One").json()
    client.put(f"/api/appointments/{second['id']}", json={"status": "completed"})
    resp = client.get("/api/appointments", params={"status": "completed"})
    names = [a["patient_name"] for a in resp.json()]
    assert names == ["Done One"]


def test_search_filter_matches_patient(client):
    _create(client, patient_name="Aarav Mehta")
    _create(client, patient_name="Sana Qureshi")
    resp = client.get("/api/appointments", params={"search": "aarav"})
    body = resp.json()
    assert len(body) == 1
    assert body[0]["patient_name"] == "Aarav Mehta"


def test_stats_endpoint_counts(client):
    _create(client, department="Cardiology")
    done = _create(client, department="Pediatrics").json()
    client.put(f"/api/appointments/{done['id']}", json={"status": "completed"})
    resp = client.get("/api/appointments/stats")
    assert resp.status_code == 200
    stats = resp.json()
    assert stats["total"] == 2
    assert stats["scheduled"] == 1
    assert stats["completed"] == 1
    assert stats["by_department"]["Cardiology"] == 1
    assert stats["by_department"]["Pediatrics"] == 1
