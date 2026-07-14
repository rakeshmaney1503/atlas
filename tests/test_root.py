from fastapi.testclient import TestClient

from atlas.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "application": "Atlas",
        "version": "0.1.0",
        "status": "running",
    }
