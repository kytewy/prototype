"""
Tests for database connections and functionality
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_neo4j_db():
    """Mock Neo4j database connection"""
    with patch("app.routers.database.get_neo4j_db") as mock:
        mock_db = AsyncMock()
        mock_db.execute_query = AsyncMock(return_value=[{"test": 1}])
        mock.return_value = mock_db
        yield mock_db


@pytest.fixture
def mock_lance_db():
    """Mock LanceDB database connection"""
    with patch("app.routers.database.get_lance_db") as mock:
        mock_db = AsyncMock()
        mock_db.db = "mock_db"
        mock.return_value = mock_db
        yield mock_db


def test_database_health(mock_neo4j_db, mock_lance_db):
    """Test database health endpoint"""
    response = client.get("/database/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data
    # Status checks deferred to Phase 2
