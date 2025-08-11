---
description:
---

# AI Legislation Tracking System Workflows

## Workflow Types

### Phase-Based

- `phase1-foundation.md` - Setup & infrastructure
- `phase2-document-ops.md` - Document management
- `phase3-llm-integration.md` - LLM capabilities
- `phase4-db-integration.md` - Database architecture
- `phase5-visualization.md` - Graph visualization
- `phase6-testing-polish.md` - Testing & production

### Task-Based

- `testing-audit.md` - Test coverage validation
- `new-feature.md` - Feature development
- `bug-fix.md` - Issue resolution
- `code-review.md` - Code quality checks

## Quick Usage Guide

1. **Follow phase workflows** in sequence
2. **Run testing audit** after each sub-phase
3. **Use task workflows** as needed during development

## Example Prompts

### Phase Workflow

```
"I'm starting Phase 1.2 (FastAPI Foundation). Let's follow @[phase1-foundation.md] workflow. What components should I implement?"
```

### Testing Audit

```
"I've completed Phase 1.2. Let's run @[testing-audit.md] to check our test coverage. What tests should we add for our FastAPI components?"
```

### New Feature

```
"Help me implement document tagging following @[new-feature.md] workflow."
```

### Bug Fix

```
"The search API returns incorrect results. Let's diagnose using @[bug-fix.md]."
```

### Code Review

```
"Review my document ingestion API implementation using @[code-review.md]."
```

## Phase Transition Requirements

- All tasks complete
- Success criteria met
- Code reviewed
- Documentation updated
- Tests passing
- Testing audit complete
