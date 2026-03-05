from app.retrieval.retriever import retrieve
from app.llm.generator import generate_answer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def build_prompt(context_chunks, query):
    context = "\n\n".join(context_chunks)
    logger.info(f"Built prompt with {len(context_chunks)} context chunks")
    return f"""

    You are a helpful assistant.
    Answer only using the provided context.
    If answer not found, say "I don't know"

    Context:
    {context}

    Question:
    {query}
    """

def handle_query(query: str, collection_name=None):
    logger.info(f"=== QUERY START ===")
    logger.info(f"Query: {query}")
    logger.info(f"Collection: {collection_name}")
    
    try:
        # Step 1: Retrieve documents
        logger.info("Step 1: Retrieving documents...")
        docs = retrieve(query, collection_name=collection_name)
        logger.info(f"Retrieved {len(docs)} documents")
        for i, doc in enumerate(docs[:3]):  # Log first 3 documents
            logger.info(f"  Doc {i+1}: {doc[:100]}...")
        
        # Step 2: Check if documents found
        if not docs:
            logger.warning("No documents found - returning fallback response")
            return {"answer": "No relevant document found"}
        
        # Step 3: Build prompt
        logger.info("Step 2: Building prompt...")
        prompt = build_prompt(docs, query)
        logger.info(f"Prompt length: {len(prompt)} characters")
        
        # Step 4: Generate answer
        logger.info("Step 3: Generating answer...")
        answer = generate_answer(prompt)
        logger.info(f"Generated answer: {answer[:100]}...")
        
        result = {"answer": answer}
        logger.info(f"QUERY COMPLETE: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        error_result = {"error": str(e), "details": "Failed to process query"}
        logger.error(f"ERROR RESULT: {error_result}")
        return error_result