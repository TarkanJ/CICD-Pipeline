import pytest

from app import app, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"

    monkeypatch.setattr("app.DATABASE", str(db_file))

    init_db()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200


def test_add_task(client):
    response = client.post(
        "/add",
        data={"task": "Learn Docker"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Learn Docker" in response.data


def test_delete_task(client):
    client.post("/add", data={"task": "Test task"})

    response = client.get("/")

    assert b"Test task" in response.data


