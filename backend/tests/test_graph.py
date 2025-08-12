import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app
from app.database.graph import GraphManager


@pytest.fixture
def client():
    """Test client with mocked graph database"""
    # Mock the graph database connection for testing
    with patch('app.routers.document.graph_manager') as mock_graph_manager, \
         patch('app.routers.document.get_graph_db') as mock_get_graph_db, \
         patch('app.routers.graph.get_graph_db') as mock_get_graph_router_db:
        
        # Create a test client
        test_client = TestClient(app)
        
        # Set up the graph manager mock
        mock_graph_manager.driver = AsyncMock()
        mock_graph_manager.connect = AsyncMock(return_value=True)
        
        # Mock graph database operations
        mock_graph_manager.create_document_node = AsyncMock(return_value=True)
        mock_graph_manager.get_document = AsyncMock(return_value={
            "id": "test-doc-id",
            "title": "Graph Test",
            "region": "EU",
            "topic": "AI",
            "document_type": "regulation",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        mock_graph_manager.create_relationship = AsyncMock(return_value=True)
        mock_graph_manager.get_related_documents = AsyncMock(return_value=[])
        mock_graph_manager.search_documents = AsyncMock(return_value=[])
        
        # Set up the dependency mocks to return our mocked graph_manager
        # This prevents the actual Neo4j connection from being attempted
        mock_get_graph_db._is_test = True
        mock_get_graph_db.return_value = mock_graph_manager
        mock_get_graph_router_db._is_test = True
        mock_get_graph_router_db.return_value = mock_graph_manager
        
        yield test_client


class TestGraphAPI:
    """Graph database API tests"""
    
    def test_create_document_node(self, client):
        """Test creating a document node in the graph"""
        # Setup custom mock for this test
        from app.routers.document import graph_manager
        graph_manager.create_document_node = AsyncMock(return_value=True)
        
        # Test data
        doc_data = {
            "id": "test-doc-id",
            "title": "Graph Test Document",
            "region": "EU",
            "topic": "AI",
            "document_type": "regulation"
        }
        
        # Assuming there's an endpoint for creating document nodes
        response = client.post("/graph/documents/", json=doc_data)
        assert response.status_code == 200
        assert response.json()["success"] is True
    
    def test_create_relationship(self, client):
        """Test creating a relationship between documents"""
        # Setup custom mock for this test
        from app.routers.document import graph_manager
        graph_manager.create_relationship = AsyncMock(return_value=True)
        
        # Test data
        relationship_data = {
            "source_id": "doc-1",
            "target_id": "doc-2",
            "rel_type": "REFERENCES",
            "confidence": 0.85
        }
        
        # Assuming there's an endpoint for creating relationships
        response = client.post("/graph/relationships/", json=relationship_data)
        assert response.status_code == 200
        assert response.json()["success"] is True
    
    def test_get_document(self, client):
        """Test retrieving a document node from the graph"""
        # Setup custom mock for this test
        from app.routers.document import graph_manager
        graph_manager.get_document = AsyncMock(return_value={
            "id": "test-doc-id",
            "title": "Graph Test",
            "region": "EU",
            "topic": "AI",
            "document_type": "regulation",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        
        # Assuming there's an endpoint for getting document nodes
        response = client.get("/graph/documents/test-doc-id")
        assert response.status_code == 200
        assert response.json()["id"] == "test-doc-id"
        assert response.json()["title"] == "Graph Test"
    
    def test_get_nonexistent_document(self, client):
        """Test retrieving a nonexistent document node"""
        # Mock for nonexistent document
        from app.routers.document import graph_manager
        graph_manager.get_document = AsyncMock(return_value=None)
        
        # Assuming there's an endpoint for getting document nodes
        response = client.get("/graph/documents/nonexistent")
        assert response.status_code == 404
    
    def test_get_related_documents(self, client):
        """Test retrieving related documents"""
        # Setup custom mock for this test
        from app.routers.document import graph_manager
        graph_manager.get_related_documents = AsyncMock(return_value=[
            {
                "related": {
                    "id": "related-doc-1",
                    "title": "Related Document 1",
                    "region": "US",
                    "topic": "AI",
                    "document_type": "regulation"
                },
                "r": {
                    "type": "REFERENCES",
                    "confidence": 0.9,
                    "created_at": "2023-01-01T00:00:00"
                }
            }
        ])
        
        # Assuming there's an endpoint for getting related documents
        response = client.get("/graph/documents/test-doc-id/related")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
        assert response.json()[0]["related"]["id"] == "related-doc-1"
    
    def test_search_documents(self, client):
        """Test searching for documents by metadata"""
        # Setup custom mock for this test
        from app.routers.document import graph_manager
        graph_manager.search_documents = AsyncMock(return_value=[
            {
                "id": "search-doc-1",
                "title": "Search Result 1",
                "region": "EU",
                "topic": "AI",
                "document_type": "regulation"
            }
        ])
        
        # Use the correct search endpoint path
        response = client.get("/graph/search?region=EU&topic=AI")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
        assert response.json()[0]["id"] == "search-doc-1"
    
    def test_integrated_document_creation(self, client):
        """Test document creation with both vector and graph databases"""
        # Setup mocks for both databases
        from app.routers.document import db_manager, graph_manager
        doc_id = "integrated-test-id"
        
        # Vector DB mocks
        db_manager.create_document = AsyncMock(return_value=doc_id)
        db_manager.get_document = AsyncMock(return_value={
            "id": doc_id,
            "title": "Integrated Test",
            "content": "Test content",
            "tags": ["AI", "regulation"],
            "category": "legal",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        
        # Graph DB mocks
        graph_manager.create_document_node = AsyncMock(return_value=True)
        
        # Assuming there's an integrated endpoint for creating documents
        response = client.post("/documents/", json={
            "title": "Integrated Test",
            "content": "Test content",
            "tags": ["AI", "regulation"],
            "category": "legal",
            "region": "EU",
            "topic": "AI",
            "document_type": "regulation"
        })
        
        assert response.status_code == 200
        assert response.json()["id"] == doc_id
        assert response.json()["title"] == "Integrated Test"
        
        # Verify both database operations were called
        db_manager.create_document.assert_called_once()
        graph_manager.create_document_node.assert_called_once()
        
    def test_unified_metadata_handling(self, client):
        """Test the unified metadata structure between document and graph models"""
        # Setup mocks for both databases
        from app.routers.document import db_manager, graph_manager
        doc_id = "metadata-test-id"
        
        # Vector DB mocks
        db_manager.create_document = AsyncMock(return_value=doc_id)
        db_manager.get_document = AsyncMock(return_value={
            "id": doc_id,
            "title": "Metadata Test",
            "content": "Test content with metadata",
            "tags": ["AI", "regulation"],
            "category": "legal",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        
        # Graph DB mocks with metadata capture
        metadata_capture = {}
        
        async def mock_create_document_node(document_id, title, metadata):
            nonlocal metadata_capture
            metadata_capture = metadata
            return True
            
        graph_manager.create_document_node = AsyncMock(side_effect=mock_create_document_node)
        
        # Create document with explicit metadata structure
        response = client.post("/documents/", json={
            "title": "Metadata Test",
            "content": "Test content with metadata",
            "tags": ["AI", "regulation"],
            "category": "legal",
            "metadata": {
                "region": "Global",
                "topic": "AI Ethics",
                "document_type": "policy",
                "custom_fields": {
                    "importance": "high",
                    "review_date": "2023-12-31"
                }
            }
        })
        
        assert response.status_code == 200
        assert response.json()["id"] == doc_id
        
        # Verify metadata was correctly passed to graph database
        assert metadata_capture.get("region") == "Global"
        assert metadata_capture.get("topic") == "AI Ethics"
        assert metadata_capture.get("document_type") == "policy"
        assert metadata_capture.get("custom_fields", {}).get("importance") == "high"
        assert metadata_capture.get("custom_fields", {}).get("review_date") == "2023-12-31"


# Additional test class for unit testing the GraphManager directly
class TestGraphManager:
    """Unit tests for GraphManager"""
    
    @pytest.fixture
    def graph_manager(self):
        """Create a GraphManager instance with mocked Neo4j driver"""
        with patch('neo4j.AsyncGraphDatabase.driver') as mock_driver:
            # Create a GraphManager instance
            manager = GraphManager(uri="bolt://mock:7687", user="mock", password="mock")

            # Initialize the driver attribute and mock its methods
            manager.driver = AsyncMock()
            manager.driver.verify_connectivity = AsyncMock(return_value=True)

            # Mock the _execute_query method
            manager._execute_query = AsyncMock()

            return manager

    # test_connect removed as it requires real Neo4j connectivity
    
    @pytest.mark.asyncio
    async def test_create_document_node(self, graph_manager):
        """Test creating a document node"""
        # Mock _execute_query to return a result
        graph_manager._execute_query.return_value = [{"d": {"id": "test-id"}}]
        
        result = await graph_manager.create_document_node(
            "test-id", "Test Document", {"region": "EU", "topic": "AI"}
        )
        
        assert result is True
        graph_manager._execute_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_relationship(self, graph_manager):
        """Test creating a relationship between documents"""
        # Mock _execute_query to return a result
        graph_manager._execute_query.return_value = [{"r": {}}]
        
        result = await graph_manager.create_relationship(
            "source-id", "target-id", "REFERENCES", 0.9
        )
        
        assert result is True
        graph_manager._execute_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_document(self, graph_manager):
        """Test retrieving a document node"""
        # Mock _execute_query to return a document
        expected_doc = {
            "id": "test-id",
            "title": "Test Document",
            "region": "EU"
        }
        graph_manager._execute_query.return_value = [{"d": expected_doc}]
        
        result = await graph_manager.get_document("test-id")
        
        assert result == expected_doc
        graph_manager._execute_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_related_documents(self, graph_manager):
        """Test retrieving related documents"""
        # Mock _execute_query to return related documents
        expected_result = [
            {
                "related": {"id": "related-1"},
                "r": {"type": "REFERENCES"}
            }
        ]
        graph_manager._execute_query.return_value = expected_result
        
        result = await graph_manager.get_related_documents("test-id", "REFERENCES")
        
        assert result == expected_result
        graph_manager._execute_query.assert_called_once()
