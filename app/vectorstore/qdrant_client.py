import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from app.ingestion.embedder import get_embedding_dimension

DEFAULT_COLLECTION_NAME = "DOCUMENTS"

_Client = None


def get_qdrant_client():
    global _Client
    if _Client is None:
        _Client = QdrantClient(host="localhost", port=6333)
    return _Client

def list_collections():
    client = get_qdrant_client()
    try:
        collections = client.get_collections()
        return [c.name for c in collections.collections]
    except Exception as e:
        print(f"Error listing collections: {e}")
        return []

def delete_collection(collection_name):
    client = get_qdrant_client()
    try:
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' deleted successfully")
        return True
    except Exception as e:
        print(f"Error deleting collection '{collection_name}': {e}")
        return False

def get_collection_info(collection_name=None):
    client = get_qdrant_client()
    collection_name = collection_name or "DOCUMENTS"
    try:
        info = client.get_collection(collection_name)
        return {
            "name": collection_name,
            "points_count": info.points_count,
            "vector_size": info.config.params.vectors.size,
            "distance": info.config.params.vectors.distance
        }
    except Exception as e:
        return {"error": str(e)}

def create_collection(collection_name=None):
    client = get_qdrant_client()
    collection_name = collection_name or DEFAULT_COLLECTION_NAME
    collections = list_collections()

    if collection_name not in collections:
       client.create_collection(
            collection_name=collection_name,
           vectors_config=VectorParams(
               size=get_embedding_dimension(),
               distance=Distance.COSINE,
           ),
          
       )
       print(f"Collection '{collection_name}' created successfully")
    else:
       print(f"Collection '{collection_name}' already exists")

def insert_chunks(chunks: list, embeddings: list, collection_name=None):
    client = get_qdrant_client()
    collection_name = collection_name or "DOCUMENTS"
    
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk},
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]
    
    client.upsert(collection_name=collection_name, points=points)
    print(f"Inserted {len(points)} chunks into collection '{collection_name}'")
