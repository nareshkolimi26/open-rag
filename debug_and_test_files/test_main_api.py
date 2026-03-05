import requests
import json

base_url = "http://localhost:8000"

def test_main_api():
    print("=== Testing Main API Endpoints ===")
    
    # Test 1: Ingestion with collection
    print("\n1. Testing ingestion with collection name...")
    with open("naresh_profile.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "test_main_collection"}
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    
    # Test 2: List collections
    print("\n2. Testing list collections...")
    response = requests.get(f"{base_url}/collections")
    print(f"Status: {response.status_code}")
    print(f"Collections: {response.json()}")
    
    # Test 3: Query with collection
    print("\n3. Testing query with collection...")
    query_data = {
        "query": "What is Naresh's background?",
        "collection_name": "test_main_collection"
    }
    response = requests.post(f"{base_url}/query", json=query_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 4: Query without collection (should use default)
    print("\n4. Testing query without collection...")
    query_data = {"query": "What is this system about?"}
    response = requests.post(f"{base_url}/query", json=query_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_main_api()
