from app.services.chunking import ChunkingService


text = """
Python is a high level programming language.
It is used for AI, machine learning and backend development.

FastAPI is a modern Python framework.
It is used to build APIs quickly.

Vector databases store embeddings for semantic search.
"""


chunker = ChunkingService(
    chunk_size=100,
    overlap_sentences=1
)


chunks = chunker.create_chunks(text)


for chunk in chunks:

    print("----------------")

    print("ID:", chunk.id)

    print("Length:", chunk.length)

    print(chunk.text)