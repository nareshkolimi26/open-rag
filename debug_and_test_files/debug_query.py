import requests
import json

url = "http://localhost:8000/query"
headers = {"Content-Type": "application/json"}
data = {"query": "What is RAG?"}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
