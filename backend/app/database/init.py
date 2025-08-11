"""
Database initialization and lifecycle management
"""
from fastapi import FastAPI

from app.database.neo4j import close_neo4j_connection
from app.database.lancedb import close_lance_connection


def init_db(app: FastAPI) -> None:
    """
    Initialize database connections and register lifecycle events
    
    Args:
        app: FastAPI application instance
    """
    @app.on_event("shutdown")
    async def shutdown_db_connections():
        """Close database connections on application shutdown"""
        # Shutdown database connections
        await close_neo4j_connection()
        close_lance_connection()
