"""
Document models for legislation tracking
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any

import pyarrow as pa
from pydantic import BaseModel, Field, field_validator

from app.models.base import ResponseBase


class DocumentType(str, Enum):
    """Document type enumeration"""
    LEGISLATION = "legislation"
    REGULATION = "regulation"
    GUIDANCE = "guidance"
    REPORT = "report"
    NEWS = "news"
    OTHER = "other"


class DocumentStatus(str, Enum):
    """Document status enumeration"""
    DRAFT = "draft"
    PUBLISHED = "published"
    AMENDED = "amended"
    REPEALED = "repealed"
    SUPERSEDED = "superseded"


class DocumentBase(BaseModel):
    """Base document model"""
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    document_type: DocumentType = Field(..., description="Type of document")
    region: str = Field(..., description="Geographic region or jurisdiction")
    source_url: Optional[str] = Field(None, description="Source URL")
    published_date: Optional[datetime] = Field(None, description="Publication date")
    status: DocumentStatus = Field(default=DocumentStatus.PUBLISHED, description="Document status")
    topics: List[str] = Field(default_factory=list, description="List of topics/tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class DocumentCreate(DocumentBase):
    """Document creation model"""
    pass


class DocumentInDB(DocumentBase):
    """Document as stored in database"""
    id: str = Field(..., description="Document ID")
    embedding: Optional[List[float]] = Field(None, description="Document embedding vector")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class Document(DocumentInDB):
    """Document model with all fields"""
    pass


class DocumentResponse(ResponseBase):
    """Document response model"""
    document: Document = Field(..., description="Document data")


class DocumentListResponse(ResponseBase):
    """Document list response model"""
    documents: List[Document] = Field(..., description="List of documents")
    count: int = Field(..., description="Total number of documents")


# PyArrow schema for LanceDB
def get_document_arrow_schema() -> pa.Schema:
    """
    Get PyArrow schema for documents table
    
    Returns:
        PyArrow schema
    """
    return pa.schema([
        pa.field('id', pa.string()),
        pa.field('title', pa.string()),
        pa.field('content', pa.string()),
        pa.field('document_type', pa.string()),
        pa.field('region', pa.string()),
        pa.field('source_url', pa.string(), nullable=True),
        pa.field('published_date', pa.timestamp('ms'), nullable=True),
        pa.field('status', pa.string()),
        pa.field('topics', pa.list_(pa.string())),
        pa.field('metadata', pa.map_(pa.string(), pa.string())),
        pa.field('embedding', pa.list_(pa.float32())),
        pa.field('created_at', pa.timestamp('ms')),
        pa.field('updated_at', pa.timestamp('ms'))
    ])
