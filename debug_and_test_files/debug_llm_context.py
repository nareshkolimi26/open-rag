from app.services.query_service import handle_query

def test_llm_context():
    print("=== Testing LLM Context ===")
    
    # Test query with collection
    result = handle_query("What is Naresh's background?", "test_collection")
    print(f"Query result: {result}")
    
    # Check if LLM is working
    if "I don't know" in result.get("answer", ""):
        print("❌ LLM is using fallback - no context provided")
    elif "Based on the context" in result.get("answer", ""):
        print("✅ LLM is working with context")
    else:
        print("ℹ️ LLM gave unexpected response")

if __name__ == "__main__":
    test_llm_context()
