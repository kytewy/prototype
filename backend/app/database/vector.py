import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
import numpy as np

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sentence_transformers import SentenceTransformer

class DatabaseManager:
    def __init__(self, db_uri: str = "postgresql+asyncpg://postgres:password@localhost:5432/hr_db"):
        self.db_uri = db_uri
        self.engine = None
        self.session_factory = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model
        
    async def connect(self):
        """Initialize database connection and create table if needed"""
        try:
            print(f"Connecting to database at {self.db_uri}")
            self.engine = create_async_engine(self.db_uri)
            self.session_factory = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
            
            # Create tables if they don't exist
            async with self.engine.begin() as conn:
                # Enable pgvector extension
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                
                # Create documents table if it doesn't exist
                await conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id VARCHAR(36) PRIMARY KEY,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        tags JSONB NOT NULL,
                        category VARCHAR(50) NOT NULL,
                        vector vector(384) NOT NULL,
                        created_at TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP NOT NULL
                    )
                """))
                
                # Create index for vector similarity search
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS documents_vector_idx 
                    ON documents USING ivfflat (vector vector_cosine_ops)
                """))
            
            print("Database connection established successfully")
            return True
        except Exception as e:
            import traceback
            print(f"Error connecting to database: {str(e)}")
            print(traceback.format_exc())
            return False
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        return self.model.encode(text).tolist()
    
    async def create_document(self, doc_data: Dict[str, Any]) -> str:
        """Create a new document"""
        try:
            if not doc_data:
                raise ValueError("Document data is empty")
            
            required_fields = ["title", "content"]
            for field in required_fields:
                if field not in doc_data:
                    raise ValueError(f"Missing required field: {field}")
            
            doc_id = str(uuid.uuid4())
            now = datetime.now()
            
            print(f"Creating document with ID: {doc_id}")
            print(f"Document data: {doc_data}")
            
            # Generate embedding from title + content
            text_for_embedding = f"{doc_data['title']} {doc_data['content']}"
            print(f"Generating embedding for text: {text_for_embedding[:50]}...")
            
            try:
                vector = self.generate_embedding(text_for_embedding)
                print(f"Generated embedding with length: {len(vector)}")
            except Exception as e:
                print(f"Error generating embedding: {str(e)}")
                raise
            
            # Ensure engine is initialized
            if self.engine is None:
                print("Engine is None, reconnecting...")
                await self.connect()
                if self.engine is None:
                    raise ValueError("Failed to initialize database connection")
            
            # Insert document into database
            async with self.session_factory() as session:
                async with session.begin():
                    query = text("""
                        INSERT INTO documents (id, title, content, tags, category, vector, created_at, updated_at)
                        VALUES (:id, :title, :content, :tags, :category, :vector, :created_at, :updated_at)
                    """)
                    
                    await session.execute(query, {
                        "id": doc_id,
                        "title": doc_data["title"],
                        "content": doc_data["content"],
                        "tags": json.dumps(doc_data.get("tags", [])),
                        "category": doc_data.get("category", "general"),
                        "vector": vector,
                        "created_at": now,
                        "updated_at": now
                    })
            
            print(f"Document added successfully: {doc_id}")
            return doc_id
        except Exception as e:
            import traceback
            print(f"Error in create_document: {str(e)}")
            print(f"Error type: {type(e)}")
            print(traceback.format_exc())
            raise
    
    async def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        try:
            async with self.session_factory() as session:
                query = text("""
                    SELECT id, title, content, tags, category, created_at, updated_at
                    FROM documents
                    WHERE id = :doc_id
                """)
                
                result = await session.execute(query, {"doc_id": doc_id})
                row = result.fetchone()
                
                if not row:
                    return None
                
                doc = dict(row)
                # Parse tags back to list
                doc["tags"] = json.loads(doc["tags"])
                # Convert datetime to string
                doc["created_at"] = doc["created_at"].isoformat()
                doc["updated_at"] = doc["updated_at"].isoformat()
                return doc
        except Exception as e:
            print(f"Error in get_document: {str(e)}")
            return None
    
    async def list_documents(self, 
                       skip: int = 0, 
                       limit: int = 100,
                       category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List documents with optional filtering"""
        try:
            async with self.session_factory() as session:
                base_query = """
                    SELECT id, title, content, tags, category, created_at, updated_at
                    FROM documents
                """
                
                params = {}
                
                if category:
                    base_query += "WHERE category = :category "
                    params["category"] = category
                
                # Apply offset and limit
                base_query += "ORDER BY created_at DESC OFFSET :skip LIMIT :limit"
                params["skip"] = skip
                params["limit"] = limit
                
                result = await session.execute(text(base_query), params)
                rows = result.fetchall()
                
                if not rows:
                    return []
                
                documents = []
                for row in rows:
                    doc = dict(row)
                    doc["tags"] = json.loads(doc["tags"])
                    # Convert datetime to string
                    doc["created_at"] = doc["created_at"].isoformat()
                    doc["updated_at"] = doc["updated_at"].isoformat()
                    documents.append(doc)
                
                return documents
        except Exception as e:
            print(f"Error in list_documents: {str(e)}")
            return []
    
    async def update_document(self, doc_id: str, update_data: Dict[str, Any]) -> bool:
        """Update document"""
        try:
            # First get the existing document
            existing_doc = await self.get_document(doc_id)
            if not existing_doc:
                return False
            
            # Prepare update values
            update_values = {"updated_at": datetime.now()}
            set_clauses = ["updated_at = :updated_at"]
            
            if "title" in update_data:
                update_values["title"] = update_data["title"]
                set_clauses.append("title = :title")
            
            if "content" in update_data:
                update_values["content"] = update_data["content"]
                set_clauses.append("content = :content")
            
            if "category" in update_data:
                update_values["category"] = update_data["category"]
                set_clauses.append("category = :category")
            
            if "tags" in update_data:
                update_values["tags"] = json.dumps(update_data["tags"])
                set_clauses.append("tags = :tags")
            
            # If title or content changed, regenerate embedding
            if "title" in update_data or "content" in update_data:
                new_title = update_data.get("title", existing_doc["title"])
                new_content = update_data.get("content", existing_doc["content"])
                text_for_embedding = f"{new_title} {new_content}"
                update_values["vector"] = self.generate_embedding(text_for_embedding)
                set_clauses.append("vector = :vector")
            
            # Build update query
            update_query = f"""
                UPDATE documents
                SET {', '.join(set_clauses)}
                WHERE id = :doc_id
            """
            
            update_values["doc_id"] = doc_id
            
            async with self.session_factory() as session:
                async with session.begin():
                    await session.execute(text(update_query), update_values)
            
            return True
        except Exception as e:
            print(f"Error in update_document: {str(e)}")
            return False
    
    async def delete_document(self, doc_id: str) -> bool:
        """Delete document"""
        try:
            async with self.session_factory() as session:
                async with session.begin():
                    delete_query = text("""
                        DELETE FROM documents
                        WHERE id = :doc_id
                    """)
                    
                    result = await session.execute(delete_query, {"doc_id": doc_id})
                    return result.rowcount > 0
        except Exception as e:
            print(f"Error in delete_document: {str(e)}")
            return False
    
    async def search_documents(self, 
                             query: str, 
                             limit: int = 10,
                             category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Vector search documents"""
        try:
            # Generate embedding for query
            query_vector = self.generate_embedding(query)
            
            # Build the search query
            base_query = """
                SELECT id, title, content, tags, category, created_at, updated_at,
                       vector <=> :query_vector AS distance
                FROM documents
            """
            
            params = {"query_vector": query_vector}
            
            if category:
                base_query += "WHERE category = :category "
                params["category"] = category
            
            # Order by vector similarity and limit results
            base_query += "ORDER BY distance LIMIT :limit"
            params["limit"] = limit
            
            async with self.session_factory() as session:
                result = await session.execute(text(base_query), params)
                rows = result.fetchall()
                
                if not rows:
                    return []
                
                documents = []
                for row in rows:
                    doc = dict(row)
                    doc["tags"] = json.loads(doc["tags"])
                    # Convert datetime to string
                    doc["created_at"] = doc["created_at"].isoformat()
                    doc["updated_at"] = doc["updated_at"].isoformat()
                    # Remove distance from response
                    doc.pop("distance", None)
                    documents.append(doc)
                
                return documents
        except Exception as e:
            print(f"Error in search_documents: {str(e)}")
            return []

# Initialize database manager with default connection string
# This will be overridden by environment variables in production
db_manager = DatabaseManager()
