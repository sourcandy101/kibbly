from fastapi.testclient import TestClient

from kibbly_ai.api.app import create_app


def test_health(settings, storage):
    client = TestClient(create_app(settings, storage))
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["storage"] == "local_json"
    assert body["llm"] == "ollama:gemma3:4b"
