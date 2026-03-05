from fastapi import APIRouter, Form
from pydantic import BaseModel
from app.services.query_service import handle_query

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    collection_name: str = None

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        result = handle_query(request.query, request.collection_name)
        return result
    except Exception as e:
        return {"error": str(e), "details": f"Failed to process query: {str(e)}"}

