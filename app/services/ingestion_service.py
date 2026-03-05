from app.ingestion.loader import load_file
from app.ingestion.chunker import chuck_text
from app.ingestion.embedder import embed_batch
from app.vectorstore.qdrant_client import insert_chunks
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ingest_document(file_bytes: bytes, filename: str, collection_name=None):
    logger.info(f"=== INGESTION START ===")
    logger.info(f"Filename: {filename}")
    logger.info(f"Collection: {collection_name}")
    
    try:
        # Step 1: Load file
        logger.info("Step 1: Loading file...")
        text = load_file(file_bytes, filename)
        logger.info(f"File loaded successfully: {len(text)} characters")
        
        # Step 2: Chunk text
        logger.info("Step 2: Chunking text...")
        chunks = chuck_text(text)
        logger.info(f"Text chunked into {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:3]):  # Log first 3 chunks
            logger.info(f"  Chunk {i+1}: {chunk[:100]}...")
        
        # Step 3: Create embeddings
        logger.info("Step 3: Creating embeddings...")
        embeddings = embed_batch(chunks)
        logger.info(f"Created {len(embeddings)} embeddings")
        
        # Step 4: Insert into collection
        logger.info("Step 4: Inserting into collection...")
        insert_chunks(chunks, embeddings, collection_name)
        logger.info(f"Successfully inserted into collection: {collection_name}")
        
        result = {"message": f"ingested {len(chunks)} chunks into collection '{collection_name or 'DOCUMENTS'}'"}
        logger.info(f"INGESTION COMPLETE: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        error_result = {"error": str(e), "details": "Failed to ingest document"}
        logger.error(f"ERROR RESULT: {error_result}")
        return error_result
