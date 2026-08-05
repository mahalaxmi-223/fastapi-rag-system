from app.services.embedding import EmbeddingService

embedding_service = EmbeddingService()

text = "FastAPI is a modern Python web framework."

embedding = embedding_service.embed(text)

print(f"Vector Dimension : {len(embedding)}")
print()
print("First 10 values:")
print(embedding[:10])