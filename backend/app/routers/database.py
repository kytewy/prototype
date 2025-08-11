"""
Database test endpoints for connection verification
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.models.base import ResponseBase
from app.database.neo4j import Neo4jDB, get_neo4j_db
from app.database.lancedb import LanceDB, get_lance_db

router = APIRouter(
    prefix="/database",
    tags=["database"],
    responses={404: {"description": "Not found"}},
)


@router.get("/health", response_model=ResponseBase)
async def database_health(
    neo4j_db: Neo4jDB = Depends(get_neo4j_db),
    lance_db: LanceDB = Depends(get_lance_db)
) -> Dict[str, Any]:
    """
    Check database connections health
    
    Returns:
        Dict: Connection status for each database
    """
    # Initialize with default values
    neo4j_status = "error"
    lance_status = "error"
    
    try:
        # Test Neo4j connection
        neo4j_result = await neo4j_db.execute_query("RETURN 1 as test")
        if neo4j_result and neo4j_result[0]["test"] == 1:
            neo4j_status = "connected"
        
        # Test LanceDB connection (just check if connected)
        if lance_db.db is not None:
            lance_status = "connected"
        
        return {
            "success": True,
            "message": "Database connections checked",
            "neo4j_status": neo4j_status,
            "lancedb_status": lance_status
        }
    except Exception as e:
        # Return error response with status keys still included
        return {
            "success": False,
            "message": f"Database connection error: {str(e)}",
            "neo4j_status": neo4j_status,
            "lancedb_status": lance_status
        }
