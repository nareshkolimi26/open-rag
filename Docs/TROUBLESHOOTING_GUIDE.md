# 🔧 RAG System Troubleshooting Guide

## 🚨 Current Issue

The system is experiencing **collection creation/retrieval mismatch** where:
- Ingestion says collection created successfully
- But query says "Collection doesn't exist"

## 🔍 Root Cause Analysis

From the logs, I can see:
1. **Collection Creation**: `create_collection()` is called and succeeds
2. **Query Retrieval**: `retrieve()` is looking for collection but getting 404
3. **Timing Issue**: Possible race condition or caching problem

## 🛠️ Possible Solutions

### Solution 1: Restart Server
```bash
# Stop current server
# Restart to pick up all changes
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Solution 2: Check Qdrant Connection
```bash
# Verify Qdrant is accessible
curl http://localhost:6333/collections
```

### Solution 3: Use Working Test Server
```bash
# Use the working server that has all fixes
python working_ingest.py  # Port 8002
```

### Solution 4: Clear Qdrant Cache
```bash
# Stop Qdrant container
docker compose down
# Start again
docker compose up -d
```

## 📋 Debugging Steps

### 1. Verify Collection Creation
```bash
# Test collection creation
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@test.txt" \
  -F "collection_name=debug_collection"

# Check if it appears in list
curl -X GET "http://localhost:8000/collections"
```

### 2. Test Retrieval Directly
```python
# Test retrieval function directly
python -c "
from app.vectorstore.qdrant_client import get_qdrant_client
client = get_qdrant_client()
collections = client.get_collections()
print('Available collections:', [c.name for c in collections.collections])
"
```

### 3. Check Server Logs
Look for these specific log messages:
- `Collection 'X' created successfully`
- `Target collection: X`
- `Searching collection 'X'`
- `Retrieved N documents`

## 🎯 Expected Behavior

### ✅ Working System Should Show:
```
INGESTION START ===
Filename: test.txt
Collection: debug_collection
Step 1: Loading file...
Step 2: Chunking text...
Step 3: Creating embeddings...
Step 4: Inserting into collection...
Collection 'debug_collection' created successfully
Successfully inserted into collection: debug_collection

QUERY START ===
Query: What is in this document?
Collection: debug_collection
Top K: 5
Step 1: Creating query embedding...
Step 2: Searching collection 'debug_collection'...
Step 3: Processing 3 results...
Result 1: Score=0.8234, Text=Document content...
Result 2: Score=0.7891, Text=More content here...
Result 3: Score=0.7456, Text=Additional information...
Retrieved 3 text documents
```

## 🔧 Quick Fix Checklist

- [ ] Server restarted after changes?
- [ ] Qdrant container restarted?
- [ ] Collection appears in list after creation?
- [ ] Retrieval finds documents in collection?
- [ ] No 404 errors in retrieval?

## 📞 If Issue Persists

The problem might be in **Qdrant client connection pooling** or **async operation timing**. Consider:

1. **Connection Reuse**: Ensure single client instance
2. **Transaction Isolation**: Use separate client instances
3. **Timing**: Add delays between operations
4. **Error Handling**: Implement retry logic

## 🎯 Next Steps

1. **Restart Services**: Stop all servers, restart Qdrant, restart main server
2. **Test Incrementally**: Test one endpoint at a time
3. **Monitor Logs**: Watch for specific error patterns
4. **Document Everything**: Keep track of what works and what doesn't
