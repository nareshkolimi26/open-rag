import requests

base_url = "http://localhost:8000"

def test_correct_collection():
    print("=== Testing with Correct Collection Name ===")
    
    # Test ingestion with test_collection (the one that actually exists)
    with open("naresh_profile.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "test_collection"}  # Use the name that actually exists
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Ingestion status: {response.status_code}")
        print(f"Response: {response.json()}")
    
    # Test query on test_collection
    print("\n=== Testing Query on test_collection ===")
    query_data = {
        "query": "What is Naresh's background?",
        "collection_name": "test_collection"  # Use the correct name
    }
    response = requests.post(f"{base_url}/query", json=query_data)
    print(f"Query status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_correct_collection()
