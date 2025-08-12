from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any, Optional
from app.database.graph import GraphManager
from app.models.graph import DocumentNode, RelationshipCreate
from app.routers.document import get_graph_db

router = APIRouter(prefix="/graph", tags=["graph"])

@router.post("/documents/", response_model=Dict[str, bool])
async def create_document_node(
    document: DocumentNode,
    graph_db: GraphManager = Depends(get_graph_db)
):
    """Create a document node in the graph database"""
    try:
        success = await graph_db.create_document_node(
            document_id=document.id,
            title=document.title,
            metadata=document.metadata.model_dump() if document.metadata else {}
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create document node")
            
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating document node: {str(e)}")

@router.post("/relationships/", response_model=Dict[str, bool])
async def create_relationship(
    relationship: RelationshipCreate,
    graph_db: GraphManager = Depends(get_graph_db)
):
    """Create a relationship between two documents"""
    try:
        success = await graph_db.create_relationship(
            source_id=relationship.source_id,
            target_id=relationship.target_id,
            rel_type=relationship.rel_type,
            confidence=relationship.confidence
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create relationship")
            
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating relationship: {str(e)}")

@router.get("/documents/{document_id}", response_model=Dict[str, Any])
async def get_document(
    document_id: str,
    graph_db: GraphManager = Depends(get_graph_db)
):
    """Get a document node from the graph database"""
    try:
        document = await graph_db.get_document(document_id)
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
            
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving document: {str(e)}")

@router.get("/documents/{document_id}/related", response_model=List[Dict[str, Any]])
async def get_related_documents(
    document_id: str,
    rel_type: Optional[str] = Query(None, description="Filter by relationship type"),
    graph_db: GraphManager = Depends(get_graph_db)
):
    """Get documents related to the specified document"""
    try:
        related_docs = await graph_db.get_related_documents(document_id, rel_type)
        
        if not related_docs:
            return []
            
        return related_docs
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving related documents: {str(e)}")

@router.get("/search", response_model=List[Dict[str, Any]])
async def search_documents(
    region: Optional[str] = Query(None, description="Filter by region"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    document_type: Optional[str] = Query(None, description="Filter by document type"),
    graph_db: GraphManager = Depends(get_graph_db)
):
    """Search for documents by metadata"""
    try:
        # Build search criteria
        criteria = {}
        if region:
            criteria["region"] = region
        if topic:
            criteria["topic"] = topic
        if document_type:
            criteria["document_type"] = document_type
            
        documents = await graph_db.search_documents(criteria)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")
