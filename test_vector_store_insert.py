from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStoreService


text = """
Python is a high level programming language.
It is widely used for artificial intelligence
and machine learning.

FastAPI is a modern Python framework.
It is used to build APIs quickly.

Vector databases store embeddings.
They are useful for semantic search.
"""


# Create services
chunker = ChunkingService()
embedding_service = EmbeddingService()
vector_store = VectorStoreService()


# Make sure collection exists
vector_store.create_collection()


# Create chunks
chunks = chunker.create_chunks(text)

print("Chunks:", len(chunks))


# Generate embeddings
texts = [chunk.text for chunk in chunks]

embeddings = embedding_service.embed_batch(texts)

print("Embeddings:", len(embeddings))


# Store everything
stored = vector_store.add_chunks(
    chunks=chunks,
    embeddings=embeddings,
    document_id="test-document-001",
)

print("Stored:", stored)