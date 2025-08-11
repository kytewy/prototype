---
trigger: glob
globs: **/*.jsx,**/*.tsx
---

# AI IDE Rules for Legislation Tracking System

## Project Context

- Always read prd.md before writing any code
- Refer to all documents in /project-docs before proceeding with code generation
- This is an AI legislation tracking system with hybrid LanceDB + Neo4j architecture using FastAPI, React, and Cytoscape.js

## Code Standards & Practices

### Python/FastAPI Backend

- Use Python 3.11+ with type hints everywhere
- Follow FastAPI best practices with Pydantic models for request/response
- Use async/await for all database and API operations
- Prefer dependency injection for database connections and services
- Use structured logging with proper log levels
- Always include error handling with appropriate HTTP status codes
- Use environment variables for configuration, never hardcode secrets

### Neo4j Integration

- Use the official neo4j Python driver with async support
- Write Cypher queries with proper parameterization to prevent injection
- Implement connection pooling and proper session management
- Use transactions for multi-step operations
- Index frequently queried properties (document_id, region, topic)
- Follow Neo4j naming conventions (PascalCase for labels, UPPER_CASE for relationships)

### LanceDB Integration

- Use async database operations where possible
- Implement proper connection management and cleanup
- Structure embeddings and metadata consistently
- Use batch operations for bulk document ingestion
- Implement proper indexing strategies for search performance

### Hybrid Database Patterns

- Always maintain data consistency between LanceDB and Neo4j
- Use shared document IDs across both systems
- Implement proper error handling for database sync operations
- Design for eventual consistency with retry mechanisms
- Cache expensive cross-database queries appropriately

### React Frontend

- Use functional components with hooks
- Implement proper error boundaries for robust UX
- Use TypeScript for type safety
- Follow React Query (TanStack Query) patterns for API state management
- Keep components focused and reusable
- Implement loading states and error handling for all API calls
- Follow the Airbnb Style Guide for code formatting
- Use PascalCase for React component file names (e.g., UserCard.tsx, not user-card.tsx)
- Prefer named exports for components
- Follow Next.js patterns and use the App Router
- Correctly determine when to use server vs. client components in Next.js
- Use Tailwind CSS for styling
- Use Shadcn UI for components
- Use React Hook Form for form handling
- Use Zod for validation
- Use React Context for state management
- Use Prisma for database access

### Cytoscape.js Integration

- Use the official Cytoscape.js library with React wrappers where appropriate
- Implement performance optimizations for graphs with 1,000+ nodes
- Use appropriate layout algorithms (force-directed, hierarchical, circular)
- Style nodes and edges based on document type and relationship strength
- Implement proper event handling for node selection and interaction
- Use extensions like cytoscape-cola or cytoscape-dagre for advanced layouts

### LLM Integration

- Always implement token usage tracking and logging
- Use structured outputs (JSON) to control LLM verbosity
- Implement proper rate limiting and retry logic
- Add cost monitoring for all LLM calls
- Use different models for different complexity levels (cheaper for simple tasks)

## Quality & Testing

- Write unit tests for all business logic
- Include integration tests for API endpoints
- Test agent workflows end-to-end
- Always validate inputs and handle edge cases
- Include proper documentation for all functions and classes

## Performance Guidelines

- Use async operations for I/O bound tasks
- Implement caching strategies for expensive operations
- Use batch processing for multiple document operations
- Monitor and optimize LLM token usage
- Profile database queries and optimize as needed

## Security & Compliance

- Never commit API keys or secrets to version control
- Validate and sanitize all user inputs
- Implement proper CORS settings
- Use HTTPS in production configurations
- Log security-relevant events for audit purposes

## Documentation Standards

- Include docstrings for all functions and classes
- Keep README files updated with setup instructions
- Document API endpoints with proper examples
- Explain complex agent workflows with diagrams or comments
- Update project docs when making architectural changes

## Error Handling

- Use custom exception classes for domain-specific errors
- Implement graceful degradation when services are unavailable
- Provide meaningful error messages for users
- Log errors with sufficient context for debugging
- Never expose internal errors to end users

## Specific Patterns to Follow

### Hybrid Database Pattern

```python
@dataclass
class Document:
    id: str
    title: str
    content: str  # Stored in LanceDB
    embedding: List[float]  # Stored in LanceDB
    region: str  # Stored in Neo4j as node property
    topic: str  # Stored in Neo4j as node property
    document_type: str  # Stored in Neo4j as node property

# Neo4j relationship creation
async def create_relationship(source_id: str, target_id: str, rel_type: str, confidence: float):
    async with driver.session() as session:
        await session.run(
            "MATCH (a:Document {id: $source}) "
            "MATCH (b:Document {id: $target}) "
            "CREATE (a)-[r:RELATES {type: $rel_type, confidence: $confidence}]->(b)",
            source=source_id, target=target_id, rel_type=rel_type, confidence=confidence
        )
```

### FastAPI Endpoint Pattern

```python
@app.post("/documents/ingest", response_model=IngestionResponse)
async def ingest_document(
    document: DocumentRequest,
    lance_db: LanceDB = Depends(get_lance_db),
    neo4j_db: Neo4jDB = Depends(get_neo4j_db)
) -> IngestionResponse:
    # Store in LanceDB first
    doc_id = await lance_db.store_document(document)
    # Create node in Neo4j
    await neo4j_db.create_document_node(doc_id, document.metadata)
    # Extract relationships asynchronously
    background_tasks.add_task(extract_relationships, doc_id)
    return IngestionResponse(document_id=doc_id)
```

### React Component Pattern

```typescript
// UserCard.tsx
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card } from '@/components/ui/card';
import { fetchUserData } from '@/lib/api';

interface UserCardProps {
	userId: string;
}

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

### Cytoscape.js Component Pattern

```typescript
const LegislationGraph = () => {
	const cyRef = useRef<any>(null);

	useEffect(() => {
		const cy = cytoscape({
			container: cyRef.current,
			elements: graphData.elements,
			style: [
				{
					selector: 'node[type="primary_law"]',
					style: { 'background-color': '#FF6B6B', shape: 'hexagon' },
				},
				{
					selector: 'edge[relationship="interprets"]',
					style: { 'line-color': '#4CAF50', 'target-arrow-shape': 'triangle' },
				},
			],
			layout: { name: 'cose', idealEdgeLength: 100 },
		});

		cy.on('tap', 'node', (event) => {
			const nodeId = event.target.id();
			setSelectedNode(nodeId);
		});
	}, [graphData]);
};
```

## Important Notes

- For any complex or critical task, ask clarification questions before proceeding
- Prioritize working proof-of-concept over perfect architecture initially
- Focus on demonstrable features that show clear value
- Always consider cost implications of LLM usage
- Implement observability from the start, don't add it later

## Guardrails

- Never implement features that bypass relationship confidence scoring
- Always include proper citations with graph relationship evidence
- Limit LLM response lengths to prevent verbosity
- Require confidence scores >0.7 for automatic relationship storage
- Never store or log sensitive personal information
- Always implement proper error handling for database synchronization failures
- Use transactions for operations that modify both databases
- Implement rate limiting for expensive graph analysis operations
