# Database Schema

> **Note:** For implementation details, refer to the corresponding workflow files in `.windsurf/workflows/`.

## Database Architecture

| Database | Purpose | Implementation Phase |
|----------|---------|----------------------|
| **PostgreSQL/pgvector** | Document content, embeddings | `@[phase2-document-ops.md]` |
| **Neo4j** | Document relationships, graph analysis | `@[phase4-db-integration.md]` |

## Core Models

**Document (PostgreSQL/pgvector):**
```python
# Simplified model
class Document:
    id: str                  # Unique identifier
    title: str               # Title
    content: str             # Full text
    embedding: List[float]   # Vector embedding (pgvector)
    region: str              # Region/jurisdiction
    topic: str               # Topic category
    document_type: str       # Document type
```

**Document Node (Neo4j):**
```cypher
// Simplified structure
CREATE (d:Document {
  id: "doc-123",           // Shared ID with LanceDB
  title: "AI Act",
  region: "EU",
  topic: "AI Regulation"
})
```

### Relationship Schema (Neo4j)

**Relationships:**
```cypher
// Simplified relationship structure
CREATE (d1:Document {id: "doc-123"})-[r:RELATES_TO {
    relationship_type: "amends",  // amends, references, etc.
    confidence: 0.92             // LLM confidence score
}]->(d2:Document {id: "doc-456"})
```

**Key Enums:** `@[phase2-document-ops.md]`
```python
# Core classification enums
class DocumentType(str, Enum):  # law, regulation, directive, etc.
class Region(str, Enum):        # EU, US, UK, etc.
class Topic(str, Enum):         # AI categories, regulations, etc.
```
## API Models
**Implementation Phase:** `@[phase1-foundation.md]`, `@[phase2-document-ops.md]`

```typescript
// Core API models

// Backend (Pydantic)
class DocumentBase { title, region, topic, document_type, ... }
class DocumentCreate extends DocumentBase { content }
class DocumentInDB extends DocumentBase { id, version, timestamps }

// Frontend (TypeScript)
interface Document { id, title, region, topic, documentType, ... }
interface Relationship { sourceId, targetId, relationshipType, confidence }
```

```

## Migration & Validation
**Implementation Phase:** `@[phase1-foundation.md]`, `@[phase2-document-ops.md]`

**Migration Strategy:**
- Neo4j: Cypher scripts for schema changes
- LanceDB: Python scripts for table creation

**Key Validation Rules:**
- Unique document IDs across systems
- Valid enum values (region, topic, document_type)
- 1536-dimensional embeddings (OpenAI compatible)
- Sequential version numbers

---

*For detailed implementation, refer to the corresponding workflow files in `.windsurf/workflows/`.*

## Performance & Security
**Implementation Phase:** `@[phase4-db-integration.md]`

**Performance Optimization:**
- Neo4j: Indexes on id, region, topic, document_type
- LanceDB: Vector indexing, pre-filtering, batch operations
- Query: Parameterization, pagination, connection pooling

**Security & Backup:**
- Daily automated backups with recovery testing
- Parameterized queries to prevent injection
- Proper access controls and data encryption

---

*For detailed implementation, refer to the corresponding workflow files in `.windsurf/workflows/`.*

---

*For implementation details, refer to the corresponding workflow files in `.windsurf/workflows/`.*
