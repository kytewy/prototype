---
trigger: always_on
---

# AI Legislation Tracking System Guidelines

## Project Context

- Read prd.md and /project-docs before coding
- Hybrid LanceDB + Neo4j architecture with FastAPI, React, and Cytoscape.js

## Backend (Python/FastAPI)

- Python 3.11+ with type hints
- FastAPI with Pydantic models
- Async/await for DB operations
- Dependency injection
- Structured logging and error handling
- Environment variables for config
- **See detailed rules in:** `.windsurf/rules/fastapi.md`

## Database Integration

### Neo4j

- Official async driver
- Parameterized Cypher queries
- Connection pooling
- Transactions for multi-step operations
- Index frequent properties
- PascalCase labels, UPPER_CASE relationships

### LanceDB

- Async operations
- Proper connection management
- Consistent embedding structure
- Batch operations for ingestion
- Optimize indexing for search
- **See detailed rules in:** `.windsurf/rules/lancedb.md`

### Hybrid Pattern

- Maintain consistency between databases
- Shared document IDs
- Error handling for sync operations
- Eventual consistency with retries
- Cache expensive cross-DB queries

## Frontend (React)

- TypeScript and functional components
- Next.js App Router (server/client components)
- TanStack Query for data fetching
- React Hook Form + Zod for forms
- React Context for state
- Tailwind CSS + Shadcn UI
- Airbnb Style Guide
- PascalCase component files
- Named exports
- Prisma for DB access
- **See detailed rules in:** `.windsurf/rules/react.md`

## Cytoscape.js

- React wrappers
- Performance for 1,000+ nodes
- Appropriate layout algorithms
- Style based on node/edge types
- Proper event handling
- Extensions for advanced layouts

## LLM Integration

- Token usage tracking
- Structured JSON outputs
- Rate limiting and retries
- Cost monitoring
- Model selection by complexity

## Example Patterns

```python
# Hybrid Database Document
@dataclass
class Document:
    id: str
    title: str
    content: str  # LanceDB
    embedding: List[float]  # LanceDB
    region: str  # Neo4j property
    topic: str  # Neo4j property
    document_type: str  # Neo4j property

# FastAPI Endpoint
@app.post("/documents/ingest", response_model=IngestionResponse)
async def ingest_document(
    document: DocumentRequest,
    lance_db: LanceDB = Depends(get_lance_db),
    neo4j_db: Neo4jDB = Depends(get_neo4j_db)
) -> IngestionResponse:
    doc_id = await lance_db.store_document(document)
    await neo4j_db.create_document_node(doc_id, document.metadata)
    background_tasks.add_task(extract_relationships, doc_id)
    return IngestionResponse(document_id=doc_id)
```

```typescript
// React Component
export const UserCard = ({ userId }: UserCardProps) => {
	const { data, isLoading, error } = useQuery({
		queryKey: ['user', userId],
		queryFn: () => fetchUserData(userId),
	});

	if (isLoading) return <Card className="p-4">Loading...</Card>;
	if (error)
		return <Card className="p-4 text-red-500">Error loading user</Card>;

	return (
		<Card className="p-4">
			<h3 className="text-lg font-medium">{data.name}</h3>
			<p className="text-gray-500">{data.email}</p>
		</Card>
	);
};
```

## Guardrails

- Require confidence scores >0.7 for relationships
- Include citations with graph evidence
- Limit LLM response lengths
- No sensitive personal information
- Transaction safety for dual-DB operations
- Rate limiting for expensive operations
