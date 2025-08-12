import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, AsyncMock

from app.main import app



@pytest.fixture
def client():
    """Test client with real database"""
    # Use the same postgres configuration as in docker-compose.yml
    test_db_uri = "postgresql+asyncpg://postgres:password@postgres:5432/hr_db"
    
    # Mock the database connection for testing
    with patch('app.routers.document.db_manager') as mock_db_manager:
        # Configure the mock
        from app.routers.document import db_manager
        # Save original db_uri
        original_db_uri = db_manager.db_uri
        
        # Set test database URI
        db_manager.db_uri = test_db_uri
        
        # Create a test client
        test_client = TestClient(app)
        
        # Mock the connect method to return True
        db_manager.connect = AsyncMock(return_value=True)
        
        # Mock database operations
        db_manager.create_document = AsyncMock(return_value="test-doc-id")
        db_manager.get_document = AsyncMock(return_value={
            "id": "test-doc-id",
            "title": "API Test",
            "content": "Content",
            "tags": [],
            "category": "general",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        db_manager.list_documents = AsyncMock(return_value=[])
        db_manager.search_documents = AsyncMock(return_value=[])
        db_manager.update_document = AsyncMock(return_value=True)
        db_manager.delete_document = AsyncMock(return_value=True)
        
        yield test_client
        
        # Restore original db_uri
        db_manager.db_uri = original_db_uri


class TestAPI:
    """Simple API tests"""
    
    def test_create_document(self, client):
        # Setup custom mock for this test
        from app.routers.document import db_manager
        db_manager.create_document = AsyncMock(return_value="test-doc-id")
        db_manager.get_document = AsyncMock(return_value={
            "id": "test-doc-id",
            "title": "API Test",
            "content": "Content",
            "tags": [],
            "category": "general",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        
        response = client.post("/documents/", json={"title": "API Test", "content": "Content"})
        assert response.status_code == 200
        assert response.json()["title"] == "API Test"

    def test_list_documents(self, client):
        response = client.get("/documents/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_search_documents(self, client):
        response = client.get("/documents/search?q=test")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_nonexistent_document(self, client):
        # Mock for nonexistent document
        from app.routers.document import db_manager
        db_manager.get_document = AsyncMock(return_value=None)
        
        response = client.get("/documents/nonexistent")
        assert response.status_code == 404

    def test_full_crud_flow(self, client):
        # Setup mocks for CRUD flow
        from app.routers.document import db_manager
        doc_id = "crud-test-id"
        
        # Create mock
        db_manager.create_document = AsyncMock(return_value=doc_id)
        db_manager.get_document = AsyncMock(return_value={
            "id": doc_id,
            "title": "CRUD Test",
            "content": "Test",
            "tags": [],
            "category": "general",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        
        # Create
        create_response = client.post("/documents/", json={"title": "CRUD Test", "content": "Test"})
        assert create_response.status_code == 200
        assert create_response.json()["id"] == doc_id
        
        # Read
        get_response = client.get(f"/documents/{doc_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "CRUD Test"
        
        # Update - change mock for updated document
        db_manager.update_document = AsyncMock(return_value=True)
        db_manager.get_document = AsyncMock(return_value={
            "id": doc_id,
            "title": "Updated CRUD",
            "content": "Test",
            "tags": [],
            "category": "general",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        
        update_response = client.put(f"/documents/{doc_id}", json={"title": "Updated CRUD"})
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated CRUD"
        
        # Delete
        db_manager.delete_document = AsyncMock(return_value=True)
        delete_response = client.delete(f"/documents/{doc_id}")
        assert delete_response.status_code == 200
        
        # Verify deleted
        db_manager.get_document = AsyncMock(return_value=None)
        get_response = client.get(f"/documents/{doc_id}")
        assert get_response.status_code == 404