from app.llm.generator import generate_answer, USE_REAL_GEMINI, client
import os

print(f"Using Real Gemini: {USE_REAL_GEMINI}")
print(f"API Key Present: {'GOOGLE_API_KEY' in os.environ}")

if USE_REAL_GEMINI and client:
    print("\nAvailable models:")
    try:
        models = client.models.list()
        for model in models:
            print(f"  - {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

# Test with a simple prompt
test_prompt = """
You are a helpful assistant.
Answer only using the provided context.
If answer not found, say "I don't know"

Context:
This is a test context about artificial intelligence and machine learning.

Question:
What is this context about?
"""

print("\nTesting LLM response:")
response = generate_answer(test_prompt)
print(f"Response: {response}")
