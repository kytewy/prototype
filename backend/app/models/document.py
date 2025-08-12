"""
Document models for legislation tracking
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    tags: Optional[List[str]] = Field(default_factory=list, description="Document tags")
    category: Optional[str] = Field(default="general", description="Document category")


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# PostgreSQL Schema (for reference)
# CREATE TABLE documents (
#     id VARCHAR(36) PRIMARY KEY,
#     title TEXT NOT NULL,
#     content TEXT NOT NULL,
#     tags JSONB NOT NULL,
#     category VARCHAR(50) NOT NULL,
#     vector vector(384) NOT NULL,
#     created_at TIMESTAMP NOT NULL,
#     updated_at TIMESTAMP NOT NULL
# )

