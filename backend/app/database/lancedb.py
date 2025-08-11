"""
LanceDB database connection and utility functions
"""
import os
from typing import Dict, List, Optional, Any, Union, Tuple

import lancedb
import numpy as np
import pyarrow as pa
from lancedb.embeddings import EmbeddingFunction
from lancedb.pydantic import LanceModel, Vector


class LanceDB:
    """LanceDB database connection manager"""
    
    def __init__(self, path: str = None):
        """
        Initialize LanceDB connection
        
        Args:
            path: Local path to LanceDB storage (defaults to env var)
        """
        self.path = path or os.getenv("LANCE_DB_PATH", "/app/lance_db")
        self.db = None
        self.connection = None
        
    async def connect(self, db_name: str = "legislation_db") -> None:
        """
        Connect to LanceDB using local path
        
        Args:
            db_name: Database name to use
        """
        try:
            # Ensure directory exists
            os.makedirs(self.path, exist_ok=True)
            # Connect to local LanceDB
            self.connection = lancedb.connect(self.path)
            self.db = self.connection.create_database(db_name)
        except Exception as e:
            # Re-raise the exception
            raise
    
    def close(self) -> None:
        """Close LanceDB connection"""
        if self.connection:
            self.connection.close()
            logger.info("LanceDB connection closed")
    
    async def create_table_if_not_exists(
        self, 
        table_name: str, 
        schema: pa.Schema
    ) -> Any:
        """
        Create a table if it doesn't exist
        
        Args:
            table_name: Name of the table to create
            schema: PyArrow schema for the table
            
        Returns:
            LanceDB table
        """
        if not self.db:
            await self.connect()
            
        try:
            if table_name in self.db.table_names():
                logger.info(f"Table {table_name} already exists")
                return self.db.open_table(table_name)
            
            logger.info(f"Creating table {table_name}")
            return self.db.create_table(table_name, schema=schema)
        except Exception as e:
            logger.error(f"Error creating table {table_name}: {str(e)}")
            raise
    
    async def search_documents(
        self,
        table_name: str,
        query_vector: List[float],
        limit: int = 10,
        filter_expr: Optional[str] = None,
        metric: str = "cosine"
    ) -> List[Dict[str, Any]]:
        """
        Search documents by vector similarity
        
        Args:
            table_name: Name of the table to search
            query_vector: Query embedding vector
            limit: Maximum number of results to return
            filter_expr: Optional filter expression
            metric: Distance metric (cosine, euclidean, dot)
            
        Returns:
            List of matching documents
        """
        if not self.db:
            await self.connect()
            
        try:
            table = self.db.open_table(table_name)
            query = table.search(query_vector).limit(limit).metric(metric)
            
            if filter_expr:
                query = query.where(filter_expr)
                
            results = query.to_list()
            return results
        except Exception as e:
            logger.error(f"Error searching table {table_name}: {str(e)}")
            raise


# Singleton instance
_lance_db: Optional[LanceDB] = None


async def get_lance_db() -> LanceDB:
    """
    Get LanceDB database connection
    
    Returns:
        LanceDB instance
    """
    global _lance_db
    if _lance_db is None:
        _lance_db = LanceDB()
        await _lance_db.connect()
    return _lance_db


def close_lance_connection() -> None:
    """Close LanceDB connection on shutdown"""
    global _lance_db
    if _lance_db:
        _lance_db.close()
        _lance_db = None
