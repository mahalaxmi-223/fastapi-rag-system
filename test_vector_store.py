from app.services.vector_store import VectorStoreService


vector_store = VectorStoreService()

print("Before:", vector_store.collection_exists())

vector_store.create_collection()

print("After:", vector_store.collection_exists())