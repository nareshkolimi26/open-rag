# Qdrant Collections and Parallel Processing Guide

## Overview
Your RAG system now supports:
- **Multiple Collections**: Organize documents by topic, source, or user
- **Parallel Processing**: Ingest multiple documents simultaneously
- **Collection Management**: Create, list, delete, and get info

## API Endpoints

### 1. Single File Ingestion with Collection
```bash
POST /ingest
Content-Type: multipart/form-data

Parameters:
- file: (required) - File to ingest
- collection_name: (optional) - Collection name (defaults to "DOCUMENTS")
```

### 2. Parallel Ingestion
```bash
POST /ingest-parallel
Content-Type: multipart/form-data

Parameters:
- files: (required) - Multiple files to ingest
- collection_names: (optional) - Comma-separated collection names
```

### 3. Collection Management
```bash
GET /collections                    # List all collections
DELETE /collections/{name}          # Delete collection
GET /collections/{name}/info        # Get collection info
```

## Usage Examples

### Example 1: Create Specific Collections
```bash
# Upload resume to "resume" collection
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@resume.pdf" \
  -F "collection_name=resume"

# Upload technical docs to "tech_docs" collection
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@technical_docs.pdf" \
  -F "collection_name=tech_docs"
```

### Example 2: Parallel Ingestion
```bash
# Upload multiple files to different collections
curl -X POST "http://localhost:8000/ingest-parallel" \
  -F "files=@resume.pdf" \
  -F "files=@technical_docs.pdf" \
  -F "files=@project_notes.txt" \
  -F "collection_names=resume,tech_docs,notes"
```

### Example 3: Collection Management
```bash
# List all collections
curl -X GET "http://localhost:8000/collections"

# Get collection info
curl -X GET "http://localhost:8000/collections/resume/info"

# Delete collection
curl -X DELETE "http://localhost:8000/collections/old_collection"
```

## Benefits

### 1. Organization
- Separate documents by type: `resumes`, `technical_docs`, `projects`
- Separate by user: `user_1_docs`, `user_2_docs`
- Separate by topic: `agriculture`, `technology`, `business`

### 2. Performance
- **Parallel Processing**: Up to 4x faster ingestion
- **Concurrent Access**: Multiple collections can be queried simultaneously
- **Scalability**: Easy to add new document categories

### 3. Management
- **Selective Queries**: Query specific collections for faster results
- **Easy Cleanup**: Delete entire collections when no longer needed
- **Monitoring**: Track collection sizes and statistics

## Testing
Run the test script to verify functionality:
```bash
python test_parallel_collections.py
```

## Qdrant Studio Access
View your collections at: `http://localhost:6333/dashboard`

## Best Practices
1. **Naming Convention**: Use descriptive names (e.g., `user_resumes_2024`)
2. **Collection Size**: Keep collections under 10K documents for optimal performance
3. **Parallel Limits**: Use max 4 concurrent uploads for best results
4. **Regular Cleanup**: Delete unused collections to save space
