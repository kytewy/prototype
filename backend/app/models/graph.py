"""
Neo4j graph models for document nodes and relationships
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.document import DocumentMetadata


class RelationshipType(str, Enum):
    """Types of relationships between documents"""
    REFERENCES = "REFERENCES"
    AMENDS = "AMENDS"
    IMPLEMENTS = "IMPLEMENTS"
    SUPERSEDES = "SUPERSEDES"
    RELATED_TO = "RELATED_TO"


class DocumentNode(BaseModel):
    """Document node in Neo4j graph"""
    id: str
    title: str
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def region(self) -> str:
        """Get region from metadata"""
        return self.metadata.region
    
    @property
    def topic(self) -> str:
        """Get topic from metadata"""
        return self.metadata.topic
    
    @property
    def document_type(self) -> str:
        """Get document type from metadata"""
        return self.metadata.document_type


class RelationshipCreate(BaseModel):
    """Input model for creating a relationship between documents"""
    source_id: str
    target_id: str
    rel_type: str
    confidence: float = 0.0


class DocumentRelationship(BaseModel):
    """Relationship between document nodes"""
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    confidence: float = 0.0
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)


class GraphQueryResult(BaseModel):
    """Result of a graph query"""
    nodes: List[DocumentNode] = []
    relationships: List[DocumentRelationship] = []
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
