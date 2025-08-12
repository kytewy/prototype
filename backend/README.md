# AI Legislation Tracking System - Backend

This is the backend service for the AI Legislation Tracking System, built with FastAPI, PostgreSQL/pgvector, and Neo4j.

## Technology Stack

- **FastAPI**: Modern, high-performance web framework for building APIs
- **PostgreSQL/pgvector**: Vector database for document storage and similarity search
- **Neo4j**: Graph database for document relationships and network analysis
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **SentenceTransformer**: For generating document embeddings

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+

### Running the Backend

The backend is containerized and can be run using Docker Compose:

```bash
# Start all services
docker-compose up -d

# Start only the backend service
docker-compose up -d backend
```

### Environment Variables

The backend service uses the following environment variables (configured in docker-compose.yml):

- `POSTGRES_URI`: PostgreSQL connection string
- `NEO4J_URI`: Neo4j connection string
- `NEO4J_USERNAME`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Manual Testing

### Using FastAPI Docs

1. Start the services: `docker-compose up -d`
2. Open http://localhost:8000/docs in your browser
3. Use the interactive Swagger UI to test API endpoints:
   - Create a document: POST `/documents`
   - Get a document: GET `/documents/{document_id}`
   - List documents: GET `/documents`
   - Search documents: GET `/documents/search`
   - Update a document: PUT `/documents/{document_id}`
   - Delete a document: DELETE `/documents/{document_id}`

### Using curl

```bash
# Create a document
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Document","content":"This is a test document","tags":[],"category":"general"}'

# Get a document
curl -X GET "http://localhost:8000/documents/{document_id}"

# Search documents
curl -X GET "http://localhost:8000/documents/search?query=test"
```

## Database Access

### PostgreSQL/pgvector

You can connect to the PostgreSQL database directly:

```bash
# Connect to PostgreSQL container
docker-compose exec postgres psql -U postgres -d hr_db

# Basic pgvector commands
SELECT * FROM documents;
SELECT * FROM documents ORDER BY embedding <-> '[0.1, 0.2, ...]'::vector LIMIT 5;
```

### Neo4j

Access the Neo4j browser at http://localhost:7474 with:
- Username: neo4j
- Password: password (as configured in docker-compose.yml)

## Running Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest tests/test_document.py -v

# Run with coverage
docker-compose exec backend pytest --cov=app
```

## Development

### Project Structure

```
backend/
├── app/
│   ├── database/         # Database connections and operations
│   │   └── vector.py     # PostgreSQL/pgvector operations
│   ├── models/           # Pydantic models
│   │   └── document.py   # Document models
│   ├── routers/          # API routes
│   │   ├── document.py   # Document endpoints
│   │   └── health.py     # Health check endpoint
│   └── main.py           # Application entry point
├── tests/                # Test files
└── requirements.txt      # Python dependencies
```

### Adding New Endpoints

1. Create a new router file in `app/routers/`
2. Add models in `app/models/` if needed
3. Include the router in `app/main.py`
