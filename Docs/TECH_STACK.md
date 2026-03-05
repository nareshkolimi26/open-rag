# 🌐 OpenRAG – Tech Stack Documentation

## 📌 Overview

OpenRAG is a fully open-source Retrieval-Augmented Generation (RAG) system designed to provide document-grounded AI responses using local LLMs and self-hosted infrastructure.

This document describes the technology stack used in the project and the reasoning behind each selection.

---

# 🏗 Architecture Overview

User → FastAPI → Embedding Model → Qdrant →  
Retrieve Top-K → Prompt Builder → Local LLM (Ollama) → Response

---

# 🧩 Core Technology Stack

## 1️⃣ Backend Framework

**FastAPI**
- High performance (ASGI-based)
- Async support
- Automatic OpenAPI docs
- Lightweight and modular

Why chosen:
- Ideal for AI APIs
- Clean structure
- Easy dependency injection

---

## 2️⃣ Vector Database

**Qdrant (Self-hosted via Docker)**

- Rust-based high performance
- Native vector similarity search
- Metadata filtering
- Production-ready
- Easy scaling

Similarity Metric:
- Cosine similarity

Why chosen:
- Fully open-source
- Easy Docker deployment
- Good Python client support

---

## 3️⃣ Embedding Model

**BGE (BAAI General Embeddings)**

- Lightweight
- Strong semantic similarity performance
- Open-source
- Supports multilingual (optional upgrade)

Why chosen:
- Good accuracy-to-size ratio
- Can run locally
- No API cost

---

## 4️⃣ Large Language Model (LLM)

**Google Gemini API**

- **Model**: `gemini-2.5-flash`
- **Integration**: `google-genai` Python client
- **Features**: High-quality text generation, context-aware responses
- **Performance**: Fast response times with good reasoning
- **Fallback**: Intelligent mock responses when API fails

**Configuration:**
```python
import google.genai as genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
```

**Why chosen:**
- High-quality text generation with good reasoning
- Fast response times for real-time applications
- Reliable API with excellent uptime
- Context-aware responses for RAG systems
- Intelligent fallback system for reliability

**Key Features:**
- Real-time text generation
- Context-aware responses
- Fast inference speed
- Reliable API service
- Built-in safety filters
- Multi-language support

**Fallback Strategy:**
- Automatic fallback to mock responses when API fails
- Context-aware mock answers based on retrieved documents
- Graceful degradation for system reliability

---

## 5️⃣ Orchestration Layer

Custom modular architecture:
- Ingestion pipeline
- Retrieval layer
- LLM integration
- Service layer

Future extension:
- LangChain or LlamaIndex (optional)

---

## 6️⃣ Containerization

**Docker + Docker Compose**

- Qdrant container
- Application container (future)
- Easy environment replication

Future:
- Kubernetes deployment

---

## 7️⃣ Configuration Management

- python-dotenv
- Centralized settings class
- Environment-based configuration

---

# 🔐 Security (Planned)

- JWT Authentication
- Role-Based Access Control (RBAC)
- Rate limiting
- Input validation

---

# 📊 Evaluation (Planned)

- Precision@K
- Recall@K
- Latency tracking
- Hallucination monitoring

---

# 📦 Deployment Strategy

Stage 1:
- Local development

Stage 2:
- Dockerized app

Stage 3:
- Kubernetes deployment (EKS / On-Prem)

---

# 🚀 Future Enhancements

- Hybrid search (BM25 + Vector)
- Cross-encoder reranking
- Redis caching
- Multi-tenant collections
- Multilingual query support
- Streaming responses
- Observability (Prometheus + Grafana)

---

# 🏆 Design Principles

- Fully open-source stack
- Modular architecture
- Swappable components

---

# 📌 Summary

OpenRAG is designed as a scalable, secure, and production-ready RAG system using:

- FastAPI (Web Framework)
- Qdrant (Vector Database)
- BGE embeddings (SentenceTransformers)
- Google Gemini API (LLM)
- Docker (Containerization)

This stack ensures high performance, reliability, and scalability while maintaining production-grade architecture with intelligent fallback systems.