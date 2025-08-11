"""
Test configuration and fixtures
"""
import os
import sys
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

# Add the parent directory to sys.path to allow importing 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(autouse=True)
def mock_db_connections():
    """
    Mock database connections for all tests
    """
    # Mock Neo4j connection
    with patch("app.database.neo4j.Neo4jDB.execute_query") as mock_neo4j_query:
        mock_neo4j_query.return_value = [{"test": 1}]
        
        # Mock LanceDB connection
        with patch("app.database.lancedb.LanceDB.connect") as mock_lance_connect:
            # Mock database initialization
            with patch("app.database.init.init_db"):
                yield
