from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import traceback

app = FastAPI()

@app.post("/debug-ingest")
async def debug_ingest(file: UploadFile = File(...), collection_name: str = None):
    try:
        content = await file.read()
        print(f"File received: {file.filename}")
        print(f"Collection name: {collection_name}")
        print(f"File size: {len(content)} bytes")
        
        # Simple response
        return JSONResponse({
            "message": f"Debug: Received {file.filename}",
            "collection": collection_name,
            "size": len(content)
        })
        
    except Exception as e:
        print(f"Error in debug endpoint: {e}")
        print(traceback.format_exc())
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
def root():
    return {"message": "debug server running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
