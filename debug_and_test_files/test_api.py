import requests
import json

base_url = "http://localhost:8000"

def test_minimal_ingestion():
    print("=== Testing Minimal Ingestion ===")
    
    # Test with simple file
    test_content = "This is a test document about artificial intelligence."
    
    # Create a mock file upload
    files = {"file": ("test.txt", test_content, "text/plain")}
    data = {"collection_name": "test_collection"}
    
    try:
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ Ingestion successful!")
        else:
            print("✗ Ingestion failed")
            
    except Exception as e:
        print(f"✗ Error: {e}")

def test_query():
    print("\n=== Testing Query ===")
    
    query_data = {
        "query": "What is this test document about?",
        "collection_name": "test_collection"
    }
    
    try:
        response = requests.post(f"{base_url}/query", json=query_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_minimal_ingestion()
    test_query()
