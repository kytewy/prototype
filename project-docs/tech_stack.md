# Tech Stack Reference

> **Note:** For implementation details and specific tasks, refer to the corresponding workflow files in `.windsurf/workflows/`. This document provides a high-level overview of the technology choices.

## Backend Architecture

**Core Framework:** FastAPI
**Implementation Phase:** `@[phase1-foundation.md]`
- Python web framework with async support and automatic API documentation
- See `.windsurf/rules/fastapi.md` for detailed implementation guidelines

**Hybrid Database Architecture:**
**Implementation Phase:** `@[phase2-document-ops.md]`, `@[phase4-db-integration.md]`
- **PostgreSQL/pgvector:** Vector database for document content, embeddings, and metadata
- **Neo4j:** Graph database for document relationships and network analysis
- See `.windsurf/rules/lancedb.md` for detailed implementation guidelines (Note: Now using pgvector instead)

**LLM Integration:**
**Implementation Phase:** `@[phase3-llm-integration.md]`
- OpenAI-compatible API with cost optimization strategies
- LangFuse for observability, tracing, and cost tracking

## Frontend Architecture

### Core Framework

- **React** - JavaScript library
  - Version: Latest stable with hooks
  - Build tool: Vite (fast development)
  - Styling: Tailwind CSS (rapid prototyping)

**State Management:**
- React Context API, TanStack Query, React Hook Form
- TypeScript and Zod for type safety and validation

## Development Tools

### API Development

- **FastAPI automatic docs** - Swagger/OpenAPI
- **Pydantic** - Data validation and serialization
- **Python type hints** - Code clarity and IDE support

### Testing

- **Backend:** pytest, pytest-asyncio
- **Frontend:** Jest, React Testing Library
- **Integration:** Playwright for E2E testing

### Code Quality

- **Python:** black (formatting), ruff (linting), mypy (type checking)
- **JavaScript:** ESLint, Prettier
- **Pre-commit hooks** for consistent code quality

## Data Flow
**Implementation Phase:** `@[phase2-document-ops.md]`, `@[phase3-llm-integration.md]`, `@[phase4-db-integration.md]`

```
Document Ingestion → LanceDB (content + embeddings) → LLM Analysis → Neo4j (relationships)

User Query → Hybrid Search (LanceDB + Neo4j) → Combined Results with Citations
```

## API Design Patterns

### RESTful Endpoints

- `POST /documents/ingest` - Document ingestion with relationship extraction
- `GET /search/hybrid` - Semantic + graph search combination
- `GET /search/semantic` - Pure vector similarity search
- `GET /search/graph` - Pure graph traversal queries
- `GET /graph/data` - Graph visualization data (nodes + edges)
- `GET /graph/analysis/{type}` - Network analysis (centrality, clustering, paths)
- `GET /documents/{id}` - Retrieve specific document with relationships
- `GET /relationships/{source}/{target}` - Relationship details between documents
- `GET /health` - System health check

### Graph-Specific Endpoints

- `GET /graph/centrality` - Document importance analysis
- `GET /graph/communities` - Document clustering results
- `GET /graph/paths` - Multi-hop regulatory connections
- `POST /graph/query` - Custom Cypher query execution

### WebSocket Support (Future)

- Real-time query processing updates
- Agent workflow status

## Deployment Considerations

### Development

- **Docker** - Containerization
- **Docker Compose** - Local multi-service setup (FastAPI + Neo4j + LanceDB)
- **Python virtual environments** - Dependency isolation

### Production (Future)

- **Cloud providers:** AWS, GCP, or Azure
- **Graph Database:** Neo4j Aura (managed) or self-hosted clusters
- **Container orchestration:** Kubernetes
- **Monitoring:** Prometheus + Grafana + Neo4j metrics
- **Load balancing:** nginx or cloud load balancer

## Security & Compliance

### API Security

- Rate limiting
- Input validation and sanitization
- HTTPS only
- CORS configuration

### Data Security

- Document encryption at rest (future)
- Audit logging
- Access controls (future)

## Performance Optimization

### Backend

- **Async operations** - FastAPI native support
- **Connection pooling** - Neo4j and LanceDB connections
- **Graph query optimization** - Cypher query planning, indexed properties
- **Relationship caching** - Redis for frequent graph traversals (future)
- **Batch processing** - Bulk relationship extraction and updates

### Frontend

- **Code splitting** - React lazy loading
- **Graph rendering optimization** - Cytoscape.js performance tuning
- **Virtual scrolling** - Large document lists
- **Canvas rendering** - For large graph visualizations (1,000+ nodes)

## Cost Management

### LLM Usage

- **Model selection** - Cheaper models for simple classification tasks
- **Relationship extraction optimization** - Batch similar document pairs
- **Prompt caching** - Reuse analysis patterns for similar documents
- **Usage monitoring** - LangFuse cost tracking with alerts

### Infrastructure

- **Neo4j optimization** - Index frequently queried properties
- **Graph partitioning** - Distribute large graphs across nodes (future)
- **Query result caching** - Cache expensive graph traversals
- **Monitoring** - Track query performance and relationship extraction costs

## Environment Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Authentication
JWT_SECRET=your-secret-key
NEXTAUTH_SECRET=your-nextauth-secret

# External Services
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG...

# App Configuration
NODE_ENV=development
PORT=3000
```

### Configuration Files

- `.env.local` - Local development
- `.env.staging` - Staging environment
- `.env.production` - Production environment

## Performance Targets

### Frontend

- **First Contentful Paint:** < 1.5s
- **Largest Contentful Paint:** < 2.5s
- **Cumulative Layout Shift:** < 0.1
- **Bundle Size:** < 500KB gzipped

### Backend

- **API Response Time:** < 200ms (95th percentile)
- **Database Query Time:** < 100ms average
- **Uptime:** 99.9% availability

## Security Considerations

### Frontend Security

- Content Security Policy (CSP)
- XSS protection via sanitization
- HTTPS only in production

### Backend Security

- Input validation and sanitization
- Rate limiting
- SQL injection prevention
- Secure session management

---

_Keep this document updated as the tech stack evolves and new tools are adopted._
