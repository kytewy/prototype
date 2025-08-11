from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_ping():
    """Test the new health check endpoint"""
    response = client.get("/health/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
