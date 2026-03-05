import requests
import json
import time

base_url = "http://localhost:8000"

def test_complete_pipeline():
    print("=== COMPLETE PIPELINE TEST WITH LOGGING ===")
    print("Start your main server with: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("Then run this test in another terminal...")
    print()
    
    # Step 1: Clean slate
    print("\n1. Cleaning up...")
    try:
        response = requests.delete(f"{base_url}/collections/test_logging_collection")
        print(f"Delete status: {response.status_code}")
    except:
        print("Delete failed (collection may not exist)")
    
    time.sleep(1)
    
    # Step 2: Ingest document
    print("\n2. Ingesting document...")
    with open("naresh_profile.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "test_logging_collection"}
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Ingestion response: {response.json()}")
    
    time.sleep(2)
    
    # Step 3: Query document
    print("\n3. Querying document...")
    query_data = {
        "query": "What is Naresh's technical background?",
        "collection_name": "test_logging_collection"
    }
    response = requests.post(f"{base_url}/query", json=query_data)
    print(f"Query response: {response.json()}")
    
    print("\n=== CHECK SERVER LOGS FOR DETAILED STEPS ===")
    print("The server console will show:")
    print("- INGESTION logs: File loading, chunking, embedding creation, insertion")
    print("- QUERY logs: Retrieval steps, document processing, LLM generation")
    print("- Look for any ERROR messages or warnings")

if __name__ == "__main__":
    test_complete_pipeline()
