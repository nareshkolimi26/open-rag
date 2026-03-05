import requests

# Test basic server health
try:
    response = requests.get("http://localhost:8000/")
    print(f"Server health: {response.json()}")
except:
    print("Server not responding")

# Test ingestion with collection name
try:
    with open("naresh_profile.txt", "rb") as f:
        files = {"file": f}
        data = {"collection_name": "test_collection"}
        response = requests.post("http://localhost:8000/ingest", files=files, data=data, timeout=10)
        print(f"Ingestion status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        else:
            print(f"Success: {response.json()}")
except Exception as e:
    print(f"Ingestion error: {e}")
