"""Backend temel testleri."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    """Root endpoint sağlık kontrolü."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_health_check():
    """Health endpoint kontrolü."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
