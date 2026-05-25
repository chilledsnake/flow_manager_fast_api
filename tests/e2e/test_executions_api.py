def test_execute_successful_flow(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    resp = client.post("/api/v1/flow/flow123/execute")
    assert resp.status_code == 202
    data = resp.json()
    assert data["status"] == "completed"
    assert len(data["results"]) == 3
    assert data["results"]["task1"]["status"] == "success"
    assert data["results"]["task1"]["output"]["raw_data"] == [1, 2, 3]
    assert data["results"]["task2"]["output"]["processed_data"] == [10, 20, 30]
    assert data["results"]["task3"]["output"]["stored"] is True


def test_execute_nonexistent_flow_returns_404(client):
    resp = client.post("/api/v1/flow/missing/execute")
    assert resp.status_code == 404


def test_execute_flow_preserves_definition_snapshot(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    exec_resp = client.post("/api/v1/flow/flow123/execute")
    execution_id = exec_resp.json()["id"]
    sample_flow["flow"]["name"] = "Updated flow"
    client.put("/api/v1/flow/flow123", json=sample_flow)
    resp = client.get(f"/api/v1/execution/{execution_id}/")
    assert resp.json()["flow_def"]["name"] == "Data processing flow"


def test_get_existing_execution(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    exec_resp = client.post("/api/v1/flow/flow123/execute")
    execution_id = exec_resp.json()["id"]
    resp = client.get(f"/api/v1/execution/{execution_id}/")
    assert resp.status_code == 200
    assert resp.json()["id"] == execution_id


def test_get_nonexistent_execution_returns_404(client):
    resp = client.get("/api/v1/execution/missing/")
    assert resp.status_code == 404


def test_list_all_executions(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    client.post("/api/v1/flow/flow123/execute")
    resp = client.get("/api/v1/execution/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_list_executions_filtered_by_flow(client, sample_flow):
    import copy

    client.post("/api/v1/flow/", json=sample_flow)
    other_flow = copy.deepcopy(sample_flow)
    other_flow["flow"]["id"] = "flow456"
    other_flow["flow"]["name"] = "Other flow"
    client.post("/api/v1/flow/", json=other_flow)

    client.post("/api/v1/flow/flow123/execute")
    client.post("/api/v1/flow/flow456/execute")
    client.post("/api/v1/flow/flow123/execute")

    resp = client.get("/api/v1/execution/", params={"flow_id": "flow123"})
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 2
    assert all(r["flow_id"] == "flow123" for r in results)


def test_list_executions_filtered_by_flow_no_match(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    client.post("/api/v1/flow/flow123/execute")

    resp = client.get("/api/v1/execution/", params={"flow_id": "nonexistent"})
    assert resp.status_code == 200
    assert resp.json() == []
