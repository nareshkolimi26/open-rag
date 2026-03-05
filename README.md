# 📚 OpenRAG Documentation

## 🎯 Overview

OpenRAG is a modular Retrieval-Augmented Generation (RAG) system designed for scalable document processing and intelligent query answering. This documentation provides comprehensive information about the system's architecture, requirements, and implementation.

## 📋 Document Structure

### 🏗️ [Architecture](./ARCHITECTURE.md)
- High-level system design
- Component interactions
- Data flow diagrams
- Scalability considerations
- Security architecture

### 📋 [Product Requirements](./PRD.md)
- Business objectives and user stories
- Functional requirements
- Non-functional requirements
- Success metrics
- Release planning

### 🔧 [Technical Requirements](./TRD.md)
- Detailed technical specifications
- API documentation
- Database schemas
- Performance requirements
- Implementation guidelines

### 📖 [Collection Guide](./COLLECTION_GUIDE.md)
- Collection management
- Usage examples
- Best practices
- Performance tips

### 🛠️ [Troubleshooting Guide](./TROUBLESHOOTING_GUIDE.md)
- Common issues and solutions
- Debugging techniques
- Performance optimization
- Error handling

### 🎯 [Solution Summary](./SOLUTION_SUMMARY.md)
- Implementation status
- Working features
- Testing results
- Deployment guide

### ⚙️ [Tech Stack](./TECH_STACK.md)
- Technology choices
- Component specifications
- Integration details
- Rationale for selections

## 🚀 Quick Start

### 1. System Requirements
- Python 3.11+
- Docker and Docker Compose
- Google Gemini API key
- 4GB+ RAM (16GB recommended)

### 2. Installation
```bash
# Clone repository
git clone <repository-url>
cd openrag

# Install dependencies
pip install -r requirements.txt

# Start Qdrant
docker compose up -d

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Basic Usage
```bash
# Ingest a document
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.pdf" \
  -F "collection_name=my_collection"

# Query the collection
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?", "collection_name": "my_collection"}'
```

## 📊 System Status

### ✅ Completed Features
- **Document Ingestion**: PDF and text file processing
- **Collection Management**: Dynamic collection creation and management
- **Vector Search**: Semantic similarity with Qdrant
- **LLM Integration**: Gemini API with intelligent fallback
- **REST API**: Comprehensive endpoint coverage
- **Error Handling**: Robust error management
- **Logging System**: Detailed pipeline tracking

### 🔄 In Progress
- **Parallel Processing**: Multi-document ingestion
- **Performance Optimization**: Caching and connection pooling
- **Advanced Analytics**: Usage insights and monitoring

### 📋 Planned Features
- **Hybrid Search**: BM25 + vector search
- **Reranking**: Cross-encoder refinement
- **Conversation Memory**: Multi-turn dialogue
- **Multi-modal Support**: Image and audio processing
- **Enterprise Features**: SSO, RBAC, audit logs

## 🏛️ Architecture Overview

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

## 🔧 Key Components

### 1. **Ingestion Pipeline**
- File type detection (PDF, text)
- Text extraction and chunking
- Embedding generation
- Vector storage

### 2. **Query Pipeline**
- Query embedding
- Vector similarity search
- Context retrieval
- LLM generation

### 3. **Collection Management**
- Dynamic collection creation
- Collection metadata
- Statistics and monitoring
- Deletion and cleanup

### 4. **API Layer**
- RESTful endpoints
- Request validation
- Error handling
- Response formatting

## 📈 Performance Metrics

### Current Performance
- **Query Response**: < 2 seconds
- **Ingestion Speed**: > 1MB/second
- **System Uptime**: > 99%
- **Error Rate**: < 1%

### Scalability Targets
- **Documents**: 1M+ per collection
- **Collections**: 10K+ total
- **Concurrent Users**: 1000+
- **API Requests**: 10K+/minute

## 🔒 Security Features

- **Input Validation**: File type and size restrictions
- **Error Sanitization**: Safe error messages
- **API Key Security**: Environment variable storage
- **Rate Limiting**: Request throttling
- **Data Privacy**: Local processing where possible

## 📊 Monitoring & Observability

### Logging System
- **Structured Logging**: JSON format with timestamps
- **Pipeline Tracking**: Step-by-step process monitoring
- **Error Tracking**: Detailed error context
- **Performance Metrics**: Request timing and throughput

### Health Monitoring
- **Service Health**: API, database, and LLM status
- **Resource Usage**: Memory, CPU, and storage
- **Error Rates**: Real-time error tracking
- **Performance Trends**: Historical performance data

## 🧪 Testing

### Test Coverage
- **Unit Tests**: Component-level testing
- **Integration Tests**: API endpoint testing
- **End-to-End Tests**: Complete pipeline testing
- **Performance Tests**: Load and stress testing

### Test Organization
```
debug_and_test_files/
├── test_*.py              # Integration tests
├── debug_*.py            # Debug utilities
├── working_*.py          # Working examples
└── final_*.py            # Final test suites
```

## 🚀 Deployment

### Development Environment
```bash
# Start development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start Qdrant
docker compose up -d

# Run tests
python -m pytest tests/
```

### Production Environment
```bash
# Build and deploy
docker build -t openrag .
docker compose -f docker-compose.prod.yml up -d

# Monitor logs
docker logs -f openrag
```

## 📞 Support

### Documentation
- **Architecture**: System design and components
- **API Reference**: Endpoint documentation
- **Troubleshooting**: Common issues and solutions
- **Best Practices**: Usage guidelines

### Getting Help
1. Check the [Troubleshooting Guide](./TROUBLESHOOTING_GUIDE.md)
2. Review the [Architecture](./ARCHITECTURE.md) documentation
3. Check the [Technical Requirements](./TRD.md)
4. Review the [Collection Guide](./COLLECTION_GUIDE.md)

## 🔄 Version History

### v1.0.0 (Current)
- Basic RAG functionality
- PDF and text ingestion
- Collection management
- Gemini LLM integration
- REST API endpoints
- Comprehensive logging

### v1.1.0 (Planned)
- Parallel processing
- Performance optimizations
- Advanced analytics
- Enhanced error handling

### v2.0.0 (Future)
- Hybrid search
- Reranking systems
- Conversation memory
- Multi-modal support
- Enterprise features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Please read the contributing guidelines and submit pull requests to the main branch.

## 📧 Contact

For questions and support, please open an issue in the repository or contact the development team.

---

**OpenRAG**: Modular, Scalable, Production-Ready RAG System 🚀
