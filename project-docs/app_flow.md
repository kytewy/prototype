# Application Flow

## Overview
Wire-frame level tour focused on agent behavior and core functionality for demo purposes.

> **Note:** For implementation details, refer to the corresponding workflow files in `.windsurf/workflows/`.

## Page Structure

| Page Type | Implementation Phase | Agent Behavior |
|-----------|----------------------|----------------|
| **Document Management** | `@[phase2-document-ops.md]` | Document Ingestion, Metadata Extraction |
| **Search & Visualization** | `@[phase3-search-viz.md]` | Query Processing, Graph Analysis |
| **Analytics & Reports** | `@[phase5-analytics.md]` | Relationship Extraction, Quality Assurance |

### Core Pages

**Main Application Pages:**
- Landing (`/`) - System overview and quick access to features
- Dashboard (`/dashboard`) - Document statistics and recent activity
- Document Management (`/documents/*`) - Upload, process, and view documents
- Search (`/search`) - Natural language querying with citation support
- Visualization (`/graph`) - Interactive relationship exploration

## Agent Interaction Flow

**Multi-Agent Pipeline:**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Document        │     │ Metadata        │     │ Relationship     │
│ Ingestion Agent │────>│ Extraction Agent│────>│ Extraction Agent│
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                       │
        v                        v                       v
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Quality         │     │ Graph           │     │ Query           │
│ Assurance Agent │<────│ Analysis Agent  │<────│ Processing Agent│
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## API Structure

**Core Endpoints:**
```
/api/documents/*  - Document ingestion and management
/api/search/*     - Natural language query processing
/api/graph/*      - Knowledge graph operations
/api/agents/*     - Agent status and coordination
```

## Key Flows

**Document Processing:**
```
Upload → Extract Metadata → Generate Embeddings → Store → Extract Relationships → Build Graph
```

**Query Processing:**
```
Natural Language Query → Parse Intent → Retrieve Context → Generate Response → Provide Citations
```

**Visualization Flow:**
```
Select Parameters → Generate Graph → Interact with Nodes → View Document Details → Export Findings
```

---

*For detailed implementation, refer to the corresponding workflow files in `.windsurf/workflows/`.*
