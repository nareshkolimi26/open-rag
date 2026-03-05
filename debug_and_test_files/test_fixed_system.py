import requests
import json

base_url = "http://localhost:8000"

def test_fixed_system():
    print("=== TESTING FIXED SYSTEM ===")
    
    # Step 1: Test ingestion with logging
    print("\n1. Testing ingestion with logging...")
    with open("naresh_profile.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "fixed_test_collection"}
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Ingestion Response: {response.json()}")
    
    # Step 2: Test query with collection
    print("\n2. Testing query with collection...")
    query_data = {
        "query": "What is Naresh's technical background?",
        "collection_name": "fixed_test_collection"
    }
    response = requests.post(f"{base_url}/query", json=query_data)
    print(f"Query Response: {response.json()}")
    
    # Step 3: Test query without collection (should use default)
    print("\n3. Testing query without collection (default)...")
    query_data_default = {
        "query": "What is this system about?"
    }
    response_default = requests.post(f"{base_url}/query", json=query_data_default)
    print(f"Default Query Response: {response_default.json()}")
    
    print("\n=== ANALYSIS ===")
    if "Naresh" in response.json().get("answer", ""):
        print("✅ SUCCESS: Collection-based query working!")
    else:
        print("❌ ISSUE: Collection query not working properly")
    
    print("\n=== CHECK SERVER LOGS ===")
    print("Check your server console for detailed logging output...")

if __name__ == "__main__":
    test_fixed_system()
