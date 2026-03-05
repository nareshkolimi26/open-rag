import requests
import json

# Test collection management
base_url = "http://localhost:8000"

def test_collections():
    print("=== Testing Collection Management ===")
    
    # List existing collections
    response = requests.get(f"{base_url}/collections")
    if response.status_code == 200:
        print("Existing collections:", response.json())
    
    # Create collections with different documents
    print("\n=== Testing Single File Ingestion ===")
    
    # Test with collection name
    with open("naresh_profile.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "naresh_profile"}
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Naresh Profile: {response.json()}")
    
    with open("technical_skills.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "technical_skills"}
        response = requests.post(f"{base_url}/ingest", files=files, data=data)
        print(f"Technical Skills: {response.json()}")
    
    # Get collection info
    print("\n=== Collection Info ===")
    for collection in ["naresh_profile", "technical_skills"]:
        response = requests.get(f"{base_url}/collections/{collection}/info")
        if response.status_code == 200:
            print(f"{collection}: {response.json()}")

def test_parallel_ingestion():
    print("\n=== Testing Parallel Ingestion ===")
    
    # Prepare multiple files
    files = []
    file_names = ["naresh_profile.txt", "technical_skills.txt"]
    
    for file_name in file_names:
        with open(file_name, "rb") as f:
            files.append(("files", f))
    
    # Collection names
    collection_names = "profile_collection,skills_collection"
    
    data = {"collection_names": collection_names}
    
    response = requests.post(f"{base_url}/ingest-parallel", files=files, data=data)
    print(f"Parallel ingestion result: {response.json()}")

if __name__ == "__main__":
    test_collections()
    test_parallel_ingestion()
