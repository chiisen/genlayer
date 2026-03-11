import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_video(client):
    response = client.post(
        "/v1/video/generate",
        json={"prompt": "cat drinking coffee", "duration": 5, "ratio": "16:9"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "queued"


def test_generate_video_validation(client):
    response = client.post(
        "/v1/video/generate",
        json={}
    )
    assert response.status_code == 422


def test_get_task_not_found(client):
    response = client.get("/v1/tasks/nonexistent")
    assert response.status_code == 404
