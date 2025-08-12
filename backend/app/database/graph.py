"""
Neo4j graph database manager for document relationships
"""
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import Neo4jError


class GraphManager:
    """Neo4j graph database manager for document relationships"""
    
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        """
        Initialize Neo4j connection
        
        Args:
            uri: Neo4j connection URI (defaults to env var)
            user: Neo4j username (defaults to env var)
            password: Neo4j password (defaults to env var)
        """
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        
    async def connect(self) -> bool:
        """
        Connect to Neo4j database and initialize schema
        
        Returns:
            True if connection successful
        """
        try:
            print(f"Connecting to Neo4j at {self.uri}")
            self.driver = AsyncGraphDatabase.driver(
                self.uri, auth=(self.user, self.password)
            )
            # Test connection
            await self.driver.verify_connectivity()
            
            # Create constraints and indexes
            await self._create_schema()
            return True
        except Exception as e:
            print(f"Neo4j connection error: {e}")
            return False
    
    async def close(self) -> None:
        """Close Neo4j connection"""
        if self.driver:
            await self.driver.close()
    
    async def _create_schema(self) -> None:
        """Create constraints and indexes for the graph schema"""
        # Create constraint on Document.id (unique)
        await self._execute_query(
            "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE"
        )
        
        # Create indexes for common query fields
        await self._execute_query(
            "CREATE INDEX document_region IF NOT EXISTS FOR (d:Document) ON (d.region)"
        )
        await self._execute_query(
            "CREATE INDEX document_topic IF NOT EXISTS FOR (d:Document) ON (d.topic)"
        )
    
    async def _execute_query(
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
            print(f"Neo4j query error: {e}")
            return []
    
    async def create_document_node(
        self, document_id: str, title: str, metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Create a document node in the graph
        
        Args:
            document_id: Unique document ID (shared with pgvector)
            title: Document title
            metadata: Additional document metadata (region, topic, etc.)
            
        Returns:
            True if successful
        """
        metadata = metadata or {}
        metadata["title"] = title
        metadata["created_at"] = datetime.now().isoformat()
        
        query = """
        MERGE (d:Document {id: $id})
        SET d += $metadata,
            d.updated_at = datetime()
        RETURN d
        """
        
        result = await self._execute_query(query, {
            "id": document_id,
            "metadata": metadata
        })
        return len(result) > 0
    
    async def create_relationship(
        self, source_id: str, target_id: str, rel_type: str, 
        confidence: float = 0.0, metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Create a relationship between two document nodes
        
        Args:
            source_id: Source document ID
            target_id: Target document ID
            rel_type: Type of relationship (e.g., REFERENCES, AMENDS)
            confidence: Confidence score (0.0-1.0)
            metadata: Additional relationship metadata
            
        Returns:
            True if successful
        """
        query = f"""
        MATCH (source:Document {{id: $source_id}})
        MATCH (target:Document {{id: $target_id}})
        MERGE (source)-[r:{rel_type}]->(target)
        SET r.confidence = $confidence,
            r.created_at = datetime()
        RETURN r
        """
        
        result = await self._execute_query(query, {
            "source_id": source_id,
            "target_id": target_id,
            "confidence": confidence
        })
        return len(result) > 0
    
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document node by ID
        
        Args:
            document_id: Document ID
            
        Returns:
            Document data or None if not found
        """
        query = """
        MATCH (d:Document {id: $id})
        RETURN d
        """
        
        result = await self._execute_query(query, {"id": document_id})
        return result[0]["d"] if result else None
    
    async def get_related_documents(
        self, document_id: str, rel_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get documents related to the specified document
        
        Args:
            document_id: Document ID
            rel_type: Optional relationship type filter
            
        Returns:
            List of related documents with relationship data
        """
        rel_filter = f":{rel_type}" if rel_type else ""
        
        query = f"""
        MATCH (d:Document {{id: $id}})-[r{rel_filter}]->(related)
        RETURN related, r
        """
        
        return await self._execute_query(query, {"id": document_id})
    
    async def search_documents(
        self, filters: Dict[str, Any], limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for documents by metadata filters
        
        Args:
            filters: Dictionary of metadata filters
            limit: Maximum number of results
            
        Returns:
            List of matching documents
        """
        conditions = []
        params = {}
        
        for key, value in filters.items():
            conditions.append(f"d.{key} = ${key}")
            params[key] = value
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f"""
        MATCH (d:Document)
        WHERE {where_clause}
        RETURN d
        LIMIT {limit}
        """
        
        result = await self._execute_query(query, params)
        return [record["d"] for record in result]


# Singleton instance
graph_manager = GraphManager()
