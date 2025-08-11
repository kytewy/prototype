---
trigger: model_decision
description: Anytime lancedb or the vector database is changed
---

# LanceDB Rules

## Connection Management

- Always create one connection instance per application lifecycle using `lancedb.connect()`
- Use `lancedb.connect_async()` for async applications
- Immediately verify connectivity after connection with `db.verify_connectivity()`
- Store connection URI in environment variables, never hardcode
- Use connection pooling patterns for production applications
- Always close connections properly in application shutdown handlers

## Schema Definition

- Define schemas upfront using PyArrow types: `pa.schema([pa.field("vector", pa.list_(pa.float32(), dimension))])`
- Use Pydantic models with LanceModel for type safety: `class MyModel(LanceModel)`
- Always specify vector dimensions explicitly in schema
- Use appropriate data types: `pa.string()` for text, `pa.int64()` for IDs, `pa.timestamp("us")` for dates
- Include metadata fields for filtering and context

## Create Operations

- Use `db.create_table(name, schema=schema)` for new tables with predefined schema
- Use `db.create_table(name, data=dataframe)` to infer schema from data
- Set `mode="overwrite"` only when intentionally replacing existing tables
- Use batch inserts with `table.add(dataframe)` for multiple records
- Validate data types before insertion to prevent schema conflicts
- Use generators for large datasets to prevent memory issues

## Read Operations

- Always use `table.search(query_vector).limit(n)` to prevent unbounded results
- Specify distance metric explicitly: `.distance_type("cosine")` or `.distance_type("euclidean")`
- Use `.select(["column1", "column2"])` to limit returned columns for performance
- Apply filters with `.where("metadata_field > value", prefilter=True)` for efficiency
- Convert results appropriately: `.to_pandas()`, `.to_arrow()`, or `.to_list()`
- Use `.nprobes(n)` to tune search accuracy vs speed (5-15% of partitions)

## Update Operations

- Use `table.update(where="condition", values={"column": "new_value"})` for targeted updates
- Always include WHERE conditions to prevent updating entire table
- Use transactions for multi-step updates to maintain consistency
- Validate new values match schema before updating
- Consider recreating embeddings if source data changes significantly

## Delete Operations

- Use `table.delete(where="condition")` with specific conditions
- Always test DELETE conditions on small datasets first
- Use `table.cleanup_old_versions()` after large deletions to reclaim space
- Backup critical data before bulk delete operations
- Consider soft deletes for audit trails using status flags

## Indexing and Performance

- Create vector indices for tables with >10K records: `table.create_index(metric="cosine")`
- Set index parameters: `num_partitions=sqrt(dataset_size)`, `num_sub_vectors=dimension/16`
- Use `table.list_indices()` to monitor index status
- Create scalar indices on frequently filtered columns
- Monitor query performance and optimize based on metrics

## Error Handling

- Wrap all LanceDB operations in try-catch blocks
- Handle specific exceptions: `lancedb.LanceDBError`, `pyarrow.ArrowInvalid`
- Log connection errors with context for debugging
- Implement retry logic for transient network errors
- Validate vector dimensions before operations to prevent runtime errors

## Data Validation

- Validate vector dimensions match schema before insertion
- Check for NaN or infinite values in vectors before storage
- Ensure metadata types match schema definitions
- Validate required fields are present before operations
- Use Pydantic models for automatic validation

## Async Patterns

- Use `await db.create_table_async()` for non-blocking table creation
- Implement proper async context managers for connection cleanup
- Use `asyncio.gather()` for concurrent operations on different tables
- Always await all async LanceDB operations
- Handle async exceptions with proper error boundaries
