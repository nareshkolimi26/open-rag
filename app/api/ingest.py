from fastapi import APIRouter, UploadFile, File, Form
from app.services.ingestion_service import ingest_document

router = APIRouter()

@router.post("/ingest")
async def ingest(file: UploadFile = File(...), collection_name: str = Form(None)):
    try:
        content = await file.read()
        result = ingest_document(content, file.filename, collection_name)
        return result
    except Exception as e:
        return {"error": str(e), "details": f"Failed to ingest document: {str(e)}"}

@router.get("/collections")
def get_collections():
    try:
        from app.vectorstore.qdrant_client import list_collections
        return {"collections": list_collections()}
    except Exception as e:
        return {"error": str(e), "details": "Failed to list collections"}

@router.delete("/collections/{collection_name}")
def delete_collection(collection_name: str):
    try:
        from app.vectorstore.qdrant_client import delete_collection
        success = delete_collection(collection_name)
        return {"message": f"Collection '{collection_name}' deleted" if success else f"Failed to delete '{collection_name}'"}
    except Exception as e:
        return {"error": str(e), "details": f"Failed to delete collection '{collection_name}'"}

@router.get("/collections/{collection_name}/info")
def get_collection_info(collection_name: str):
    try:
        from app.vectorstore.qdrant_client import get_collection_info
        return get_collection_info(collection_name)
    except Exception as e:
        return {"error": str(e), "details": f"Failed to get info for collection '{collection_name}'"}
    
