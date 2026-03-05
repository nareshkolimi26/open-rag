from app.ingestion.loader import load_file
from app.ingestion.chunker import chuck_text
from app.ingestion.embedder import embed_batch

# Test the ingestion pipeline step by step
print("=== Testing Ingestion Pipeline ===")

# Step 1: Load file
with open("naresh_profile.txt", "rb") as f:
    content = f.read()
    text = load_file(content, "naresh_profile.txt")
    print(f"✓ File loaded: {len(text)} characters")

# Step 2: Chunk text
chunks = chuck_text(text)
print(f"✓ Text chunked: {len(chunks)} chunks")

# Step 3: Create embeddings
try:
    embeddings = embed_batch(chunks)
    print(f"✓ Embeddings created: {len(embeddings)} vectors")
except Exception as e:
    print(f"✗ Embedding failed: {e}")
    exit(1)

# Step 4: Test Qdrant connection
try:
    from app.vectorstore.qdrant_client import get_qdrant_client, create_collection, insert_chunks
    client = get_qdrant_client()
    collections = client.get_collections()
    print(f"✓ Qdrant connected: {[c.name for c in collections.collections]}")
except Exception as e:
    print(f"✗ Qdrant connection failed: {e}")
    exit(1)

print("\n=== All tests passed! ===")
