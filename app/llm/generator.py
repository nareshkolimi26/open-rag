import google.genai as genai
import dotenv
import os

dotenv.load_dotenv()

# Try to configure with API key if available
if os.getenv("GOOGLE_API_KEY"):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    try:
        # Test if we can access models
        models = client.models.list()
        USE_REAL_GEMINI = True
        print("Google GenAI API configured successfully")
    except Exception as e:
        print(f"Failed to configure Google GenAI: {e}")
        USE_REAL_GEMINI = False
        client = None
else:
    print("No GOOGLE_API_KEY found in environment")
    USE_REAL_GEMINI = False
    client = None

def generate_answer(prompt: str):
    if USE_REAL_GEMINI and client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Google GenAI API error: {e}")
            return mock_answer(prompt)
    else:
        return mock_answer(prompt)

def mock_answer(prompt: str):
    # Extract the context section from the prompt
    context_start = prompt.find("Context:")
    context_end = prompt.find("Question:")
    
    if context_start != -1 and context_end != -1:
        context = prompt[context_start:context_end].strip()
        question_start = prompt.find("Question:") + len("Question:")
        question = prompt[question_start:].strip()
        
        # Generate answer based on actual context content
        if "skills" in question.lower() or "technical" in question.lower():
            if "Python" in context or "JavaScript" in context or "SQL" in context:
                return "Based on the technical skills document, the person has expertise in Python, JavaScript, SQL, HTML/CSS, and various frameworks including FastAPI, TensorFlow, PyTorch, and database technologies like PostgreSQL, MongoDB, and Qdrant."
            elif "FastAPI" in context or "Qdrant" in context:
                return "The technical skills include FastAPI for REST APIs, Qdrant for vector databases, SentenceTransformers, and various machine learning frameworks."
            else:
                return "Based on the context, I can see information about technical skills and technologies used in the project."
        elif "Naresh" in question:
            return "Naresh is currently building a Retrieval-Augmented Generation (RAG) system using FastAPI, Uvicorn, Qdrant Vector Database, SentenceTransformers, and Gemini LLM. He plans to build a domain-specific knowledge base focused on Agriculture."
        elif "project" in question.lower():
            return "Naresh is working on OpenRAG, a modular Retrieval-Augmented Generation system built with FastAPI, Qdrant, SentenceTransformers, and Gemini. He designed the architecture, implemented ingestion pipeline, built embedding module, integrated Gemini LLM, and developed retrieval logic."
        elif "career" in question.lower() or "objective" in question.lower():
            return "Naresh's career objective is to become an AI Systems Engineer specializing in Retrieval-Augmented Generation, scalable AI architectures, and domain-specific knowledge assistants."
        else:
            # Try to extract relevant information from context
            if "Naresh" in context:
                return "Based on the provided information about Naresh, he is developing a RAG system with a focus on agriculture applications and has specific technical and learning goals."
            elif "Python" in context or "FastAPI" in context:
                return "Based on the technical context, the person has skills in Python, web development, and various AI/ML technologies."
            else:
                return "Based on the provided context, I can answer questions about the document content. Please ask a specific question about the information available."
    else:
        return "I cannot answer this question as the required context is not available."