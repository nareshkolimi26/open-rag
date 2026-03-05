import requests
import json

base_url = "http://localhost:8000"

def test_single_ingestion():
    print("=== Testing Single File Ingestion ===")
    
    # Test with collection name
    with open("naresh_profile.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "naresh_profile"}
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Response: {response.json()}")
    
    # Test query
    print("\n=== Testing Query ===")
    query_data = {"query": "What is Naresh's technical background?"}
    response = requests.post(f"{base_url}/query", json=query_data)
    print(f"Query Response: {response.json()}")

def test_collection_management():
    print("\n=== Testing Collection Management ===")
    
    # List collections
    response = requests.get(f"{base_url}/collections")
    print(f"Collections: {response.json()}")
    
    # Get collection info
    response = requests.get(f"{base_url}/collections/naresh_profile/info")
    print(f"Collection Info: {response.json()}")

if __name__ == "__main__":
    test_single_ingestion()
    test_collection_management()
