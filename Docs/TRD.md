# 🔧 OpenRAG Technical Requirements Document

## 📋 Overview

This Technical Requirements Document (TRD) details the technical specifications, implementation details, and technical constraints for the OpenRAG system. It serves as the technical blueprint for developers and system architects.

## 🏗️ System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Layer  │    │   API Layer     │    │   Data Layer    │
│                 │    │                 │    │                 │
│ - Web Frontend  │◄──►│ - FastAPI       │◄──►│ - Qdrant DB     │
│ - Mobile Apps   │    │ - Uvicorn       │    │ - Vector Store  │
│ - CLI Tools     │    │ - REST APIs     │    │ - Collections   │
│ - Third Party   │    │ - Validation    │    │ - Metadata      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   External      │
                       │   Services      │
                       │                 │
                       │ - Gemini LLM    │
                       │ - HuggingFace   │
                       │ - Sentence TF   │
                       └─────────────────┘
```

## 🔧 Technical Specifications

### 1. API Layer Specifications

#### 1.1 Ingestion API
```python
POST /ingest
Content-Type: multipart/form-data

Parameters:
- file: UploadFile (required) - PDF or text file
- collection_name: str (optional) - Target collection name

Response:
{
  "message": "ingested N chunks into collection 'collection_name'",
  "chunks_processed": N,
  "collection_name": "collection_name"
}

Error Response:
{
  "error": "Error message",
  "details": "Detailed error description"
}
```

#### 1.2 Query API
```python
POST /query
Content-Type: application/json

Request Body:
{
  "query": "What is the main topic?",
  "collection_name": "optional_collection_name"
}

Response:
{
  "answer": "Context-aware answer",
  "context_chunks": N,
  "collection_name": "collection_name"
}

Error Response:
{
  "error": "Error message",
  "details": "Detailed error description"
}
```

#### 1.3 Collection Management APIs
```python
GET /collections
Response: {"collections": ["collection1", "collection2", ...]}

DELETE /collections/{collection_name}
Response: {"message": "Collection 'name' deleted"}

GET /collections/{collection_name}/info
Response: {
  "name": "collection_name",
  "points_count": 1000,
  "vector_size": 384,
  "distance": "COSINE"
}
```

### 2. Data Processing Pipeline

#### 2.1 Document Processing
```python
# File Loading Pipeline
def load_file(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith('.pdf'):
        return load_pdf_file(file_bytes)
    else:
        return load_text_file(file_bytes)

# PDF Processing
def load_pdf_file(file_bytes: bytes) -> str:
    - Use PyPDF2 for text extraction
    - Handle multi-page documents
    - Preserve text structure and formatting
    - Error handling for corrupted files

# Text Processing
def load_text_file(file_bytes: bytes) -> str:
    - UTF-8 encoding with fallback
    - Handle special characters
    - Preserve line breaks and paragraphs
```

#### 2.2 Text Chunking
```python
def chuck_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    - Semantic chunking based on sentence boundaries
    - Configurable chunk size and overlap
    - Preserve context between chunks
    - Handle edge cases (very short/long documents)
```

#### 2.3 Embedding Generation
```python
def embed_batch(chunks: List[str]) -> List[List[float]]:
    - Use SentenceTransformers (all-MiniLM-L6-v2)
    - Batch processing for efficiency
    - Vector dimension: 384
    - COSINE similarity for search
    - Error handling for model failures
```

### 3. Vector Store Specifications

#### 3.1 Qdrant Configuration
```yaml
# Docker Compose Configuration
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
```

#### 3.2 Collection Schema
```python
# Vector Configuration
vectors_config = VectorParams(
    size=384,  # Embedding dimension
    distance=Distance.COSINE,  # Similarity metric
)

# Point Structure
PointStruct(
    id=str(uuid.uuid4()),  # Unique identifier
    vector=embedding,       # 384-dimensional vector
    payload={
        "text": chunk,      # Original text chunk
        "source": filename, # Source document
        "chunk_id": i,      # Chunk index
        "timestamp": datetime.now()  # Processing time
    }
)
```

### 4. LLM Integration Specifications

#### 4.1 Gemini API Integration
```python
# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

# Generation Parameters
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# Prompt Template
prompt_template = """
You are a helpful assistant.
Answer only using the provided context.
If answer not found, say "I don't know"

Context:
{context}

Question:
{query}
"""
```

#### 4.2 Fallback Strategy
```python
def generate_answer(prompt: str):
    try:
        # Try real Gemini API
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        # Fallback to mock response
        return mock_answer(prompt)
```

### 5. Performance Requirements

#### 5.1 Response Time Targets
- **Query Response**: < 2 seconds (95th percentile)
- **Ingestion**: < 10 seconds per MB
- **Collection Creation**: < 1 second
- **Embedding Generation**: < 100ms per chunk

#### 5.2 Throughput Targets
- **Concurrent Queries**: 100+ simultaneous
- **Document Ingestion**: 10+ parallel documents
- **API Requests**: 1000+ requests/minute

#### 5.3 Scalability Targets
- **Document Storage**: 1M+ documents
- **Collection Count**: 10K+ collections
- **Vector Storage**: 100GB+ embeddings
- **User Sessions**: 10K+ concurrent users

### 6. Security Specifications

#### 6.1 Input Validation
```python
# File Upload Validation
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = ['.pdf', '.txt', '.md', '.rtf']

# Query Validation
MAX_QUERY_LENGTH = 1000 characters
MIN_QUERY_LENGTH = 3 characters
SANITIZED_INPUT = remove_html_tags(query)
```

#### 6.2 Error Handling
```python
# Standardized Error Response
error_response = {
    "error": "Error type",
    "details": "Detailed description",
    "timestamp": datetime.now().isoformat(),
    "request_id": "unique_identifier"
}
```

#### 6.3 Logging Specifications
```python
# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO", "propagate": False}
    }
}
```

### 7. Database Specifications

#### 7.1 Qdrant Database
```python
# Connection Configuration
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_TIMEOUT = 30  # seconds

# Collection Configuration
DEFAULT_VECTOR_SIZE = 384
DEFAULT_DISTANCE_METRIC = "COSINE"
MAX_COLLECTIONS = 10000
MAX_POINTS_PER_COLLECTION = 1000000
```

#### 7.2 Data Models
```python
# Document Metadata
@dataclass
class DocumentMetadata:
    filename: str
    file_size: int
    file_type: str
    collection_name: str
    chunk_count: int
    processing_time: float
    created_at: datetime

# Query Result
@dataclass
class QueryResult:
    answer: str
    context_chunks: List[str]
    collection_name: str
    retrieval_time: float
    generation_time: float
    total_time: float
```

### 8. Integration Specifications

#### 8.1 External API Integrations
```python
# Gemini API
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com"
GEMINI_MODEL = "gemini-2.5-flash"
RATE_LIMIT = 60  # requests per minute

# HuggingFace (for future models)
HF_API_BASE = "https://huggingface.co"
HF_MODEL_CACHE = "./models"
```

#### 8.2 Environment Configuration
```bash
# .env file
GOOGLE_API_KEY=your_gemini_api_key
QDRANT_HOST=localhost
QDRANT_PORT=6333
LOG_LEVEL=INFO
MAX_FILE_SIZE=104857600
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 9. Testing Specifications

#### 9.1 Unit Tests
```python
# Test Coverage Requirements
MINIMUM_COVERAGE = 80%
TEST_FILES = [
    "tests/test_ingestion.py",
    "tests/test_query.py",
    "tests/test_retrieval.py",
    "tests/test_llm.py",
    "tests/test_api.py"
]
```

#### 9.2 Integration Tests
```python
# API Endpoint Tests
API_TEST_CASES = [
    "test_ingestion_pdf",
    "test_ingestion_text",
    "test_query_collection",
    "test_query_default",
    "test_collection_management",
    "test_error_handling"
]
```

#### 9.3 Performance Tests
```python
# Load Testing
CONCURRENT_USERS = 100
TEST_DURATION = 300  # seconds
RAMP_UP_TIME = 60    # seconds
```

### 10. Deployment Specifications

#### 10.1 Container Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 10.2 Docker Compose
```yaml
version: '3.8'
services:
  openrag:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - QDRANT_HOST=qdrant
    depends_on:
      - qdrant
    volumes:
      - ./logs:/app/logs

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
```

### 11. Monitoring Specifications

#### 11.1 Metrics Collection
```python
# Performance Metrics
METRICS = {
    "request_count": "Total API requests",
    "response_time": "Average response time",
    "error_rate": "Percentage of failed requests",
    "active_collections": "Number of active collections",
    "total_documents": "Total documents processed",
    "query_accuracy": "Query relevance scores"
}
```

#### 11.2 Health Checks
```python
# Health Check Endpoints
GET /health
Response: {
    "status": "healthy",
    "timestamp": "2024-02-26T18:00:00Z",
    "services": {
        "api": "healthy",
        "qdrant": "healthy",
        "llm": "healthy"
    }
}
```

### 12. Technical Constraints

#### 12.1 Resource Constraints
- **Memory**: Minimum 4GB RAM, recommended 16GB
- **Storage**: Minimum 10GB, scalable based on document volume
- **CPU**: Minimum 2 cores, recommended 8+ cores
- **Network**: Stable internet connection for LLM API

#### 12.2 Technology Constraints
- **Python Version**: 3.11+
- **Dependencies**: All from requirements.txt
- **External Services**: Gemini API, Qdrant
- **File Formats**: PDF, TXT, MD, RTF

#### 12.3 Compliance Constraints
- **Data Privacy**: No PII storage without encryption
- **API Usage**: Within Gemini API rate limits
- **Open Source**: Compatible with open-source licenses
- **Security**: Follow OWASP guidelines

## 🔄 Implementation Phases

### Phase 1: Core Functionality (Complete)
- ✅ Basic ingestion pipeline
- ✅ Vector storage and retrieval
- ✅ LLM integration
- ✅ REST API endpoints
- ✅ Error handling and logging

### Phase 2: Performance & Scale (In Progress)
- 🔄 Parallel processing
- 🔄 Connection pooling
- 🔄 Caching layer
- 🔄 Load balancing
- 🔄 Monitoring dashboard

### Phase 3: Advanced Features (Planned)
- 📋 Hybrid search
- 📋 Reranking systems
- 📋 Conversation memory
- 📋 Multi-modal support
- 📋 Enterprise features

## 📊 Technical Success Criteria

### Performance Criteria
- [ ] Query response time < 2 seconds
- [ ] Ingestion throughput > 1MB/second
- [ ] System uptime > 99.9%
- [ ] Error rate < 1%

### Quality Criteria
- [ ] Code coverage > 80%
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Security audit passed

### Scalability Criteria
- [ ] Handle 1000+ concurrent users
- [ ] Process 1M+ documents
- [ ] Support 10K+ collections
- [ ] Horizontal scaling capability

## 🚨 Risk Mitigation

### Technical Risks
1. **Qdrant Performance**: Implement proper indexing and monitoring
2. **LLM API Limits**: Rate limiting and fallback strategies
3. **Memory Issues**: Batch processing and memory optimization
4. **Network Failures**: Retry mechanisms and circuit breakers

### Operational Risks
1. **Data Loss**: Regular backups and redundancy
2. **Security Breaches**: Regular security audits
3. **Performance Degradation**: Continuous monitoring
4. **Service Downtime**: High availability setup

This TRD serves as the technical foundation for the OpenRAG system implementation and should be referenced throughout the development process.
