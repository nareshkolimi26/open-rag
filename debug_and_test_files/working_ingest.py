from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uvicorn
import os
from app.ingestion.loader import load_file
from app.ingestion.chunker import chuck_text
from app.ingestion.embedder import embed_batch
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import uuid

app = FastAPI()

# Simple Qdrant client
def get_qdrant_client():
    return QdrantClient(host="localhost", port=6333)

def create_collection_if_not_exists(collection_name):
    client = get_qdrant_client()
    try:
        collections = [c.name for c in client.get_collections().collections]
        if collection_name not in collections:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=384,  # Standard embedding size
                    distance=Distance.COSINE,
                ),
            )
            print(f"Created collection: {collection_name}")
        return True
    except Exception as e:
        print(f"Collection error: {e}")
        return False

def insert_into_collection(chunks, embeddings, collection_name):
    client = get_qdrant_client()
    try:
        points = [
            PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={"text": chunk},
                )
                for chunk, embedding in zip(chunks, embeddings)
            ]
        
        client.upsert(collection_name=collection_name, points=points)
        print(f"Inserted {len(points)} chunks into {collection_name}")
        return True
    except Exception as e:
        print(f"Insert error: {e}")
        return False

@app.post("/ingest")
async def ingest(file: UploadFile = File(...), collection_name: str = Form(None)):
    try:
        content = await file.read()
        text = load_file(content, file.filename)
        chunks = chuck_text(text)
        embeddings = embed_batch(chunks)
        
        # Use provided collection name or default
        target_collection = collection_name if collection_name else "DOCUMENTS"
        
        # Create collection if needed
        if create_collection_if_not_exists(target_collection):
            # Insert chunks
            if insert_into_collection(chunks, embeddings, target_collection):
                return JSONResponse({
                    "message": f"Successfully ingested {len(chunks)} chunks into '{target_collection}'"
                })
        else:
            return JSONResponse({"error": "Failed to create collection"}, status_code=500)
            
    except Exception as e:
        print(f"Ingestion error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
def root():
    return {"message": "working ingest server"}

@app.get("/collections")
def list_collections():
    try:
        client = get_qdrant_client()
        collections = client.get_collections()
        return {"collections": [c.name for c in collections.collections]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/query")
async def query_endpoint(query: str = Form(...), collection_name: str = Form(None)):
    try:
        client = get_qdrant_client()
        target_collection = collection_name if collection_name else "DOCUMENTS"
        
        # Embed query
        query_vectors = embed_batch([query])
        query_vector = query_vectors[0]
        
        # Search
        results = client.query_points(
            collection_name=target_collection,
            query=query_vector,
            limit=5
        )
        
        # Extract text
        documents = [hit.payload.get("text") for hit in results.points if hit.payload]
        
        if not documents:
            return {"answer": "No relevant document found"}
        
        # Simple response
        context = "\n\n".join(documents)
        answer = f"Based on the context, the answer to '{query}' can be found in the ingested documents."
        
        return JSONResponse({"answer": answer, "context": context})
        
    except Exception as e:
        print(f"Query error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
