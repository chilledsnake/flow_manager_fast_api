import copy


def test_successful_flow_end_to_end(client, sample_flow):
    create_resp = client.post("/api/v1/flow/", json=sample_flow)
    assert create_resp.status_code == 201
    assert create_resp.json()["id"] == "flow123"

    exec_resp = client.post("/api/v1/flow/flow123/execute")
    assert exec_resp.status_code == 202
    execution = exec_resp.json()
    execution_id = execution["id"]
    assert execution["status"] == "completed"
    assert execution["flow_id"] == "flow123"
    assert len(execution["results"]) == 3

    assert execution["results"]["task1"]["status"] == "success"
    assert execution["results"]["task1"]["output"]["raw_data"] == [1, 2, 3]
    assert execution["results"]["task2"]["status"] == "success"
    assert execution["results"]["task2"]["output"]["processed_data"] == [10, 20, 30]
    assert execution["results"]["task3"]["status"] == "success"
    assert execution["results"]["task3"]["output"]["stored"] is True

    get_resp = client.get(f"/api/v1/execution/{execution_id}/")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == execution_id

    list_resp = client.get("/api/v1/execution/")
    assert list_resp.status_code == 200
    assert any(e["id"] == execution_id for e in list_resp.json())

    filtered_resp = client.get("/api/v1/execution/", params={"flow_id": "flow123"})
    assert filtered_resp.status_code == 200
    assert len(filtered_resp.json()) == 1
    assert filtered_resp.json()[0]["id"] == execution_id


def test_flow_definition_snapshot_is_preserved(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    exec_resp = client.post("/api/v1/flow/flow123/execute")
    execution_id = exec_resp.json()["id"]

    sample_flow["flow"]["name"] = "Updated flow"
    client.put("/api/v1/flow/flow123", json=sample_flow)

    get_resp = client.get(f"/api/v1/execution/{execution_id}/")
    assert get_resp.json()["flow_def"]["name"] == "Data processing flow"


def test_flow_crud_and_execute(client, sample_flow):
    create_resp = client.post("/api/v1/flow/", json=sample_flow)
    assert create_resp.status_code == 201

    get_resp = client.get("/api/v1/flow/flow123")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Data processing flow"

    list_resp = client.get("/api/v1/flow/")
    assert len(list_resp.json()) == 1

    exec_resp = client.post("/api/v1/flow/flow123/execute")
    assert exec_resp.status_code == 202

    sample_flow["flow"]["name"] = "Updated flow"
    update_resp = client.put("/api/v1/flow/flow123", json=sample_flow)
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated flow"

    delete_resp = client.delete("/api/v1/flow/flow123")
    assert delete_resp.status_code == 204

    assert client.get("/api/v1/flow/flow123").status_code == 404


def test_execute_deleted_flow_returns_404(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    client.delete("/api/v1/flow/flow123")
    resp = client.post("/api/v1/flow/flow123/execute")
    assert resp.status_code == 404


def test_multiple_flows_with_filtering(client, sample_flow):
    client.post("/api/v1/flow/", json=sample_flow)
    other_flow = copy.deepcopy(sample_flow)
    other_flow["flow"]["id"] = "flow456"
    other_flow["flow"]["name"] = "Other flow"
    client.post("/api/v1/flow/", json=other_flow)

    client.post("/api/v1/flow/flow123/execute")
    client.post("/api/v1/flow/flow456/execute")
    client.post("/api/v1/flow/flow123/execute")

    all_execs = client.get("/api/v1/execution/").json()
    assert len(all_execs) == 3

    f1_execs = client.get("/api/v1/execution/", params={"flow_id": "flow123"}).json()
    assert len(f1_execs) == 2
    assert all(e["flow_id"] == "flow123" for e in f1_execs)

    f2_execs = client.get("/api/v1/execution/", params={"flow_id": "flow456"}).json()
    assert len(f2_execs) == 1
