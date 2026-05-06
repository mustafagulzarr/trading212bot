from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200


def test_sync_universe_and_fetch_universe() -> None:
    client = TestClient(app)
    sync_response = client.post('/jobs/sync-universe')
    assert sync_response.status_code == 200

    universe_response = client.get('/universe')
    assert universe_response.status_code == 200
