from fastapi.testclient import TestClient
from main import app
from src.core.database import get_session
from tests.database import override_get_session

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

def create_sample_task(title: str = "Test task", description: str = "Test desc"):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": title, "description": description},
    )
    assert response.status_code == 200
    return response.json()

def test_create_task():
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "My first task", "description": "Something"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "My first task"
    assert data["description"] == "Something"
    assert data["status"] in ["todo", "in_progress", "done"]
    assert "id" in data
    assert "created_at" in data


def test_get_tasks_list():
    create_sample_task("List task", "For listing")

    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    first = data[0]
    assert "id" in first
    assert "title" in first
    assert "status" in first


def test_get_task_by_id():
    created = create_sample_task("By ID", "Single get")
    task_id = created["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "By ID"
    assert data["description"] == "Single get"


def test_get_task_by_id_not_found():
    response = client.get("/api/v1/tasks/999999")
    assert response.status_code == 404
    data = response.json()
    assert "Task with id" in data["detail"]


def test_update_task_title_and_status():
    created = create_sample_task("Old title", "Old desc")
    task_id = created["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "New title",
            "status": "in_progress",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "New title"
    assert data["status"] == "in_progress"
    assert data["description"] == "Old desc"


def test_partial_update_only_status():
    created = create_sample_task("Partial", "Partial desc")
    task_id = created["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"status": "done"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["status"] == "done"
    assert data["title"] == "Partial"
    assert data["description"] == "Partial desc"


def test_delete_task():
    created = create_sample_task("To delete", "Will be deleted")
    task_id = created["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204
    assert response.content == b""

    response_get = client.get(f"/api/v1/tasks/{task_id}")
    assert response_get.status_code == 404
