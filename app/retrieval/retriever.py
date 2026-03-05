from app.vectorstore.qdrant_client import get_qdrant_client
from app.ingestion.embedder import embed_batch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def retrieve(query: str, top_k: int = 5, collection_name=None):
    logger.info(f"=== RETRIEVAL START ===")
    logger.info(f"Query: {query}")
    logger.info(f"Collection: {collection_name}")
    logger.info(f"Top K: {top_k}")
    
    client = get_qdrant_client()
    
    # Use default collection if None provided
    target_collection = collection_name if collection_name else "DOCUMENTS"
    logger.info(f"Target collection: {target_collection}")
    
    try:
        # Step 1: Create query embedding
        logger.info("Step 1: Creating query embedding...")
        query_vectors = embed_batch([query])
        query_vector = query_vectors[0]
        logger.info(f"Query embedding shape: {query_vector.shape if hasattr(query_vector, 'shape') else 'No shape'}")
        
        # Step 2: Search collection
        logger.info(f"Step 2: Searching collection '{target_collection}'...")
        results = client.query_points(
            collection_name=target_collection,
            query=query_vector,
            limit=top_k
        )
        
        # Step 3: Process results
        logger.info(f"Step 3: Processing {len(results.points)} results...")
        documents = []
        for i, hit in enumerate(results.points):
            text = hit.payload.get("text")
            if text:
                documents.append(text)
                logger.info(f"  Result {i+1}: Score={hit.score:.4f}, Text={text[:80]}...")
            else:
                logger.warning(f"  Result {i+1}: No text payload found")
        
        logger.info(f"Retrieved {len(documents)} text documents")
        return documents
        
    except Exception as e:
        logger.error(f"Retrieval failed: {str(e)}")
        return []
