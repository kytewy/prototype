from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from typing import List, Optional
from datetime import datetime
import os
from app.models.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.database.vector import DatabaseManager, db_manager

router = APIRouter(prefix="/documents", tags=["documents"])

async def get_db():
    """Dependency to get database manager"""
    try:
        # Initialize database connection from environment variable if available
        if os.environ.get("POSTGRES_URI") and db_manager.db_uri != os.environ.get("POSTGRES_URI"):
            db_manager.db_uri = os.environ.get("POSTGRES_URI")
            db_manager.engine = None
        
        if db_manager.engine is None or db_manager.session_factory is None:
            print("Database connection not initialized, connecting...")
            success = await db_manager.connect()
            if not success:
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to connect to database"
                )
        return db_manager
    except Exception as e:
        import traceback
        print(f"Error in get_db dependency: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Database connection error: {str(e)}"
        )

@router.post("/", response_model=DocumentResponse)
async def create_document(
    document: DocumentCreate,
    db: DatabaseManager = Depends(get_db)
):
    """Create a new document"""
    try:
        # Print debugging information
        print(f"Creating document: {document.model_dump()}")
        print(f"Database connection: {db.db_uri}")
        
        # Check if engine is initialized
        if db.engine is None:
            print("ERROR: Engine is None, attempting to reconnect")
            await db.connect()
            if db.engine is None:
                print("ERROR: Engine is still None after reconnect")
                raise ValueError("Database engine is not initialized")
        
        doc_id = await db.create_document(document.model_dump())
        print(f"Document created with ID: {doc_id}")
        
        created_doc = await db.get_document(doc_id)
        print(f"Retrieved document: {created_doc}")
        
        if not created_doc:
            raise HTTPException(status_code=500, detail="Failed to create document")
        
        return DocumentResponse(
            id=created_doc["id"],
            title=created_doc["title"],
            content=created_doc["content"],
            tags=created_doc["tags"],
            category=created_doc["category"],
            created_at=datetime.fromisoformat(created_doc["created_at"]),
            updated_at=datetime.fromisoformat(created_doc["updated_at"])
        )
    except Exception as e:
        # Print detailed error information
        import traceback
        print(f"ERROR creating document: {str(e)}")
        print(f"ERROR type: {type(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating document: {str(e)}")

@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    db: DatabaseManager = Depends(get_db)
):
    """List documents with optional filtering"""
    try:
        documents = await db.list_documents(skip=skip, limit=limit, category=category)
        return [
            DocumentResponse(
                id=doc["id"],
                title=doc["title"],
                content=doc["content"],
                tags=doc["tags"],
                category=doc["category"],
                created_at=datetime.fromisoformat(doc["created_at"]),
                updated_at=datetime.fromisoformat(doc["updated_at"])
            )
            for doc in documents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@router.get("/search", response_model=List[DocumentResponse])
async def search_documents(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = Query(None),
    db: DatabaseManager = Depends(get_db)
):
    """Vector search documents"""
    try:
        documents = await db.search_documents(query=q, limit=limit, category=category)
        return [
            DocumentResponse(
                id=doc["id"],
                title=doc["title"],
                content=doc["content"],
                tags=doc["tags"],
                category=doc["category"],
                created_at=datetime.fromisoformat(doc["created_at"]),
                updated_at=datetime.fromisoformat(doc["updated_at"])
            )
            for doc in documents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: DatabaseManager = Depends(get_db)
):
    """Get document by ID"""
    try:
        doc = await db.get_document(document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return DocumentResponse(
            id=doc["id"],
            title=doc["title"],
            content=doc["content"],
            tags=doc["tags"],
            category=doc["category"],
            created_at=datetime.fromisoformat(doc["created_at"]),
            updated_at=datetime.fromisoformat(doc["updated_at"])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting document: {str(e)}")

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    document: DocumentUpdate,
    db: DatabaseManager = Depends(get_db)
):
    """Update document"""
    try:
        # Filter out None values
        update_data = {k: v for k, v in document.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        success = await db.update_document(document_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        updated_doc = await db.get_document(document_id)
        return DocumentResponse(
            id=updated_doc["id"],
            title=updated_doc["title"],
            content=updated_doc["content"],
            tags=updated_doc["tags"],
            category=updated_doc["category"],
            created_at=datetime.fromisoformat(updated_doc["created_at"]),
            updated_at=datetime.fromisoformat(updated_doc["updated_at"])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating document: {str(e)}")

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: DatabaseManager = Depends(get_db)
):
    """Delete document"""
    try:
        success = await db.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"message": "Document deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
