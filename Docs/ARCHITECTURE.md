# 🏗️ OpenRAG System Architecture

## 📋 Overview

OpenRAG is a modular Retrieval-Augmented Generation (RAG) system designed for scalable document processing and intelligent query answering. The system combines vector search with large language models to provide context-aware responses.

## 🎯 System Purpose

- **Document Ingestion**: Process PDF and text files with automatic chunking
- **Vector Storage**: Store document embeddings in Qdrant for semantic search
- **Intelligent Retrieval**: Find relevant documents based on semantic similarity
- **Context-Aware Generation**: Generate answers using retrieved context
- **Multi-Collection Support**: Organize documents by topic, user, or domain

## 🏛️ High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │    │   FastAPI       │    │   Qdrant DB     │
│                 │    │   Backend       │    │                 │
│ - Web UI        │◄──►│ - Ingestion API │◄──►│ - Vector Store  │
│ - Mobile App    │    │ - Query API     │    │ - Collections   │
│ - CLI Tools     │    │ - Management    │    │ - Metadata      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   External APIs  │
                       │                 │
                       │ - Gemini LLM     │
                       │ - HuggingFace    │
                       │ - Sentence TF    │
                       └─────────────────┘
```

## 🔧 Core Components

### 1. **API Layer** (`app/api/`)
- **Ingestion API**: Document upload and processing
- **Query API**: Semantic search and answer generation
- **Management API**: Collection management operations

### 2. **Service Layer** (`app/services/`)
- **Ingestion Service**: Document processing pipeline
- **Query Service**: Retrieval and generation orchestration

### 3. **Processing Pipeline** (`app/ingestion/`)
- **Loader**: File type detection and content extraction
- **Chunker**: Text segmentation for optimal embedding
- **Embedder**: Vector generation using SentenceTransformers

### 4. **Retrieval System** (`app/retrieval/`)
- **Retriever**: Semantic search with Qdrant
- **Vector Operations**: Embedding similarity calculations

### 5. **LLM Integration** (`app/llm/`)
- **Generator**: Gemini API integration with fallback
- **Prompt Engineering**: Context-aware prompt building

### 6. **Vector Store** (`app/vectorstore/`)
- **Qdrant Client**: Connection and operations
- **Collection Management**: Dynamic collection handling

## 📊 Data Flow

### Ingestion Pipeline
```
Document Upload → File Loading → Text Chunking → Embedding Generation → Vector Storage
       │              │              │                   │                  │
       ▼              ▼              ▼                   ▼                  ▼
   API Endpoint   PDF/Text      Semantic       SentenceTransformers    Qdrant
   Validation     Extraction    Segmentation      Vector Creation    Collection
```

### Query Pipeline
```
User Query → Query Embedding → Vector Search → Context Retrieval → LLM Generation → Response
     │              │              │              │                  │              │
     ▼              ▼              ▼              ▼                  ▼              ▼
  API Endpoint   Semantic       Qdrant        Document Chunks      Gemini API      JSON Response
  Validation     Embedding      Search        Similarity Ranking   Context-aware   Formatted
```

## 🗂️ Collection Architecture

### Collection Types
- **Default Collection**: "DOCUMENTS" for general use
- **Named Collections**: Custom collections for specific domains
- **User Collections**: Per-user document organization
- **Topic Collections**: Domain-specific document grouping

### Collection Metadata
```json
{
  "name": "collection_name",
  "points_count": 1000,
  "vector_size": 384,
  "distance": "COSINE",
  "created_at": "2024-02-26T18:00:00Z",
  "last_updated": "2024-02-26T18:30:00Z"
}
```

## 🔌 Integration Points

### External Services
- **Qdrant Vector Database**: Local instance on port 6333
- **Gemini API**: Google's generative AI service
- **SentenceTransformers**: Local embedding model
- **HuggingFace**: Model repository and downloads

### Configuration
- **Environment Variables**: API keys and connection strings
- **Docker Compose**: Qdrant container orchestration
- **Logging**: Comprehensive system monitoring

## 🚀 Scalability Considerations

### Horizontal Scaling
- **API Servers**: Multiple FastAPI instances behind load balancer
- **Qdrant Cluster**: Distributed vector storage
- **Embedding Caching**: Redis for frequently used embeddings

### Performance Optimizations
- **Batch Processing**: Parallel document ingestion
- **Vector Indexing**: Optimized Qdrant configurations
- **Connection Pooling**: Efficient database connections
- **Async Operations**: Non-blocking I/O for better throughput

## 🔒 Security Architecture

### API Security
- **Input Validation**: File type and size restrictions
- **Error Handling**: Sanitized error responses
- **Rate Limiting**: Request throttling capabilities

### Data Security
- **Local Processing**: No data sent to external services (except LLM)
- **Environment Variables**: Secure API key storage
- **Collection Isolation**: User data separation

## 📈 Monitoring & Observability

### Logging System
- **Structured Logging**: JSON-formatted logs with timestamps
- **Pipeline Tracking**: Step-by-step process monitoring
- **Error Tracking**: Detailed error context and stack traces

### Metrics
- **Performance Metrics**: Request timing and throughput
- **System Health**: Qdrant connection status
- **Usage Analytics**: Collection sizes and query patterns

## 🔄 Deployment Architecture

### Development Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dev Server    │    │   Qdrant Dev    │    │   Local Files   │
│   Port 8000     │◄──►│   Port 6333     │◄──►│   Document      │
│   Hot Reload    │    │   Docker        │    │   Storage       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Production Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   API Cluster   │    │   Qdrant Cluster│
│                 │◄──►│   (Multiple)    │◄──►│   (Distributed) │
│   SSL/HTTPS     │    │   Auto-scaling  │    │   Replicated     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🧪 Testing Architecture

### Unit Tests
- **Component Testing**: Individual function validation
- **Mock Services**: External API mocking
- **Edge Cases**: Error condition handling

### Integration Tests
- **API Endpoints**: Full request/response cycles
- **Database Operations**: Qdrant integration testing
- **LLM Integration**: Gemini API connectivity

### End-to-End Tests
- **Document Pipeline**: Complete ingestion to query flow
- **Multi-Collection**: Cross-collection operations
- **Performance**: Load and stress testing

## 📚 Technology Stack

- **Backend**: FastAPI, Uvicorn, Python 3.11
- **Vector Database**: Qdrant (Docker)
- **Embeddings**: SentenceTransformers (BGE model)
- **LLM**: Google Gemini API
- **File Processing**: PyPDF2, Python standard library
- **Containerization**: Docker, Docker Compose
- **Development**: VS Code, Git, PowerShell

## 🎯 Future Architecture Enhancements

### Phase 2 Features
- **Hybrid Search**: BM25 + Vector search combination
- **Reranking**: Cross-encoder for result refinement
- **Conversation Memory**: Multi-turn dialogue support
- **Metadata Filtering**: Advanced search capabilities

### Phase 3 Features
- **Multi-Modal**: Image and audio processing
- **Real-time Updates**: Live document indexing
- **Advanced Analytics**: Usage insights and recommendations
- **Enterprise Features**: SSO, RBAC, audit logs
