# Phase 3: LLM Integration & Relationship Extraction

## Description
Integration of LLM capabilities for metadata extraction and relationship analysis.

## Prerequisites
- [ ] Phase 2 completed successfully
- [ ] Document storage and retrieval working
- [ ] OpenAI API access configured

## Steps

### 3.1 LLM Service Layer
```markdown
1. Create LLM service class with OpenAI integration
2. Implement prompt templates
3. Add structured output parsing (JSON)
4. Implement error handling and retries
5. Add LangFuse tracing
```

### 3.2 Metadata Extraction Pipeline
```markdown
1. Create metadata extraction service
2. Implement region classification
3. Add topic categorization
4. Extract document types
5. Add effective dates and status extraction
6. Test with diverse document samples
```

### 3.3 Relationship Analysis Engine
```markdown
1. Design relationship extraction workflow
2. Implement document similarity filtering
3. Create LLM relationship analysis prompts
4. Add relationship confidence scoring
5. Implement relationship validation
6. Add batch processing
```

## Success Criteria
- [ ] Documents automatically get metadata extracted
- [ ] Relationships are detected between related documents
- [ ] Confidence scores filter low-quality relationships
- [ ] LangFuse shows complete processing cost tracking

## Related Files
- `backend/app/services/llm_service.py`
- `backend/app/services/metadata_extractor.py`
- `backend/app/services/relationship_analyzer.py`
