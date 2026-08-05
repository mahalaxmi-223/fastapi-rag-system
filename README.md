# RAG System

A Retrieval-Augmented Generation (RAG) system that combines a vector database with a large language model to answer questions grounded in your own documents.

## Features

- Document ingestion (PDF, DOCX, TXT, Markdown)
- Configurable chunking and embedding strategies
- Pluggable vector store (ChromaDB by default, Qdrant/FAISS supported)
- FastAPI service with a `/query` endpoint and streaming responses
- Dockerized for one-command local startup

## Project Structure

```
rag-system/
├── app/          # Application source code (API, ingestion, retrieval, generation)
├── tests/        # Unit and integration tests
├── data/         # Local data, vector store persistence
├── docs/         # Source documents to index
├── .env          # Local environment variables
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Quickstart

### 1. Configure environment

Copy `.env` and fill in the values you need (at minimum an LLM provider key):

```bash
cp .env .env.local   # then edit
```

### 2. Run with Docker

```bash
docker compose up --build
```

The API will be available at http://localhost:8000, with ChromaDB at http://localhost:8001.

### 3. Run locally

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Usage

Index documents in `docs/`:

```bash
python -m app.ingest --source ./docs
```

Ask a question:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the refund policy?", "top_k": 4}'
```

## Development

```bash
pytest                     # run tests
ruff check app tests       # lint
mypy app                   # type-check
```

## License

MIT
