import requests
import json

base_url = "http://localhost:8000"

def test_full_pipeline():
    print("=== Full Pipeline Test ===")
    
    # Step 1: Clean slate - delete test_collection if exists
    print("\n1. Cleaning up...")
    try:
        response = requests.delete(f"{base_url}/collections/test_collection")
        print(f"Delete status: {response.status_code}")
    except:
        print("Delete failed or collection didn't exist")
    
    # Step 2: Ingest document
    print("\n2. Ingesting document...")
    with open("naresh_profile.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "test_collection"}
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Ingestion: {response.status_code} - {response.json()}")
    
    # Step 3: Verify collection exists
    print("\n3. Verifying collection...")
    response = requests.get(f"{base_url}/collections")
    print(f"Collections: {response.json()}")
    
    # Step 4: Test retrieval directly
    print("\n4. Testing retrieval directly...")
    from app.vectorstore.qdrant_client import get_qdrant_client
    from app.ingestion.embedder import embed_batch
    
    client = get_qdrant_client()
    query = "What is Naresh's background?"
    query_vectors = embed_batch([query])
    query_vector = query_vectors[0]
    
    try:
        results = client.query_points(
            collection_name="test_collection",
            query=query_vector,
            limit=5
        )
        print(f"Direct retrieval found: {len(results.points)} points")
        for i, hit in enumerate(results.points):
            text = hit.payload.get("text", "")
            print(f"  {i+1}. {text[:100]}...")
    except Exception as e:
        print(f"Direct retrieval error: {e}")
    
    # Step 5: Test through API
    print("\n5. Testing through API...")
    query_data = {
        "query": "What is Naresh's background?",
        "collection_name": "test_collection"
    }
    response = requests.post(f"{base_url}/query", json=query_data)
    print(f"API query result: {response.json()}")
    
    # Step 6: Analyze
    answer = response.json().get("answer", "")
    if "I don't know" in answer:
        print("❌ ISSUE: Retrieval not working through API")
    elif "Naresh" in answer:
        print("✅ SUCCESS: Full pipeline working!")
    else:
        print("ℹ️ Partial success - check context")

if __name__ == "__main__":
    test_full_pipeline()
