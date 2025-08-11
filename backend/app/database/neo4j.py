"""
Neo4j database connection and utility functions
"""
import os
from typing import AsyncGenerator, Dict, List, Optional, Any

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import Neo4jError


class Neo4jDB:
    """Neo4j database connection manager"""
    
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        """
        Initialize Neo4j connection
        
        Args:
            uri: Neo4j connection URI (defaults to env var)
            user: Neo4j username (defaults to env var)
            password: Neo4j password (defaults to env var)
        """
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        
    async def connect(self) -> None:
        """Connect to Neo4j database"""
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.uri, auth=(self.user, self.password)
            )
            # Test connection
            await self.driver.verify_connectivity()
        except Exception as e:
            # Re-raise the exception
            raise
    
    async def close(self) -> None:
        """Close Neo4j connection"""
        if self.driver:
            await self.driver.close()
    
    async def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query
        
        Args:
            query: Cypher query string
            params: Query parameters
            
        Returns:
            List of query results
        """
        if not self.driver:
            await self.connect()
            
        params = params or {}
        try:
            async with self.driver.session() as session:
                result = await session.run(query, params)
                return [record.data() for record in await result.fetch_all()]
        except Neo4jError as e:
            logger.error(f"Neo4j query error: {str(e)}")
            raise


# Singleton instance
_neo4j_db: Optional[Neo4jDB] = None


async def get_neo4j_db() -> Neo4jDB:
    """
    Get Neo4j database connection
    
    Returns:
        Neo4jDB instance
    """
    global _neo4j_db
    if _neo4j_db is None:
        _neo4j_db = Neo4jDB()
        await _neo4j_db.connect()
    return _neo4j_db


async def close_neo4j_connection() -> None:
    """Close Neo4j connection on shutdown"""
    global _neo4j_db
    if _neo4j_db:
        await _neo4j_db.close()
        _neo4j_db = None
