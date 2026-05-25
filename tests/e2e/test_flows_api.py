def test_create_flow(client, sample_flow):
    resp = client.post("/api/v1/flow/", json=sample_flow)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == "flow123"
    assert data["name"] == "Data processing flow"
    assert len(data["tasks"]) == 3


def test_create_duplicate_flow_returns_409(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    resp = client.post("/api/v1/flow/", json=sample_flow)
    assert resp.status_code == 409


def test_create_flow_invalid_start_task(client, sample_flow):
    sample_flow["flow"]["start_task"] = "nonexistent"
    resp = client.post("/api/v1/flow/", json=sample_flow)
    assert resp.status_code == 422


def test_create_flow_invalid_condition_target(client, sample_flow):
    sample_flow["flow"]["conditions"][0]["target_task_success"] = "missing_task"
    resp = client.post("/api/v1/flow/", json=sample_flow)
    assert resp.status_code == 422


def test_get_existing_flow(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    resp = client.get("/api/v1/flow/flow123")
    assert resp.status_code == 200
    assert resp.json()["id"] == "flow123"


def test_get_nonexistent_flow_returns_404(client):
    resp = client.get("/api/v1/flow/missing")
    assert resp.status_code == 404


def test_list_empty(client):
    resp = client.get("/api/v1/flow/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_with_flows(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    resp = client.get("/api/v1/flow/")
    assert len(resp.json()) == 1


def test_update_existing_flow(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    sample_flow["flow"]["name"] = "Updated flow"
    resp = client.put("/api/v1/flow/flow123", json=sample_flow)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated flow"


def test_update_nonexistent_flow_returns_404(client, sample_flow):
    resp = client.put("/api/v1/flow/missing", json=sample_flow)
    assert resp.status_code == 404


def test_delete_existing_flow(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    resp = client.delete("/api/v1/flow/flow123")
    assert resp.status_code == 204


def test_delete_nonexistent_flow_returns_404(client):
    resp = client.delete("/api/v1/flow/missing")
    assert resp.status_code == 404
