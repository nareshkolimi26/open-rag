from app.vectorstore.qdrant_client import get_qdrant_client
from app.ingestion.embedder import embed_batch

def test_retrieval():
    print("=== Testing Retrieval Debug ===")
    
    client = get_qdrant_client()
    
    # List collections
    collections = client.get_collections()
    print(f"Available collections: {[c.name for c in collections.collections]}")
    
    # Test query on test_main_collection
    collection_name = "test_main_collection"
    
    # Check if collection exists
    try:
        info = client.get_collection(collection_name)
        print(f"Collection info: {info.points_count} points")
    except Exception as e:
        print(f"Error getting collection info: {e}")
        return
    
    # Test embedding
    query = "What is Naresh's background?"
    query_vectors = embed_batch([query])
    query_vector = query_vectors[0]
    print(f"Query vector shape: {query_vector.shape if hasattr(query_vector, 'shape') else 'No shape'}")
    
    # Test search
    try:
        results = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=5
        )
        
        print(f"Search results: {len(results.points)} points found")
        for i, hit in enumerate(results.points):
            print(f"  {i+1}. Score: {hit.score}, Text preview: {hit.payload.get('text', '')[:100]}...")
            
    except Exception as e:
        print(f"Search error: {e}")

if __name__ == "__main__":
    test_retrieval()
