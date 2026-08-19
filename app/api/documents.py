from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.file_storage import FileStorageService
from app.services.pdf_parser import PDFParserService
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStoreService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


storage = FileStorageService()
parser = PDFParserService()
chunker = ChunkingService()
embedding_service = EmbeddingService()
vector_store = VectorStoreService()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    # Create unique ID for this document
    document_id = str(uuid4())

    # Step 1: Save uploaded file
    saved_path = await storage.save_file(file)

    # Step 2: Extract text from PDF
    parsed_pdf = parser.extract_text(saved_path)

    # Step 3: Create chunks
    chunks = chunker.create_chunks(parsed_pdf["text"])

    # Step 4: Extract text from each chunk
    texts = [chunk.text for chunk in chunks]

    # Step 5: Generate embeddings
    embeddings = embedding_service.embed_batch(texts)

    # Step 6: Store embeddings and chunks in Qdrant
    vector_store.create_collection()

    stored = vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document_id,
    )

    # Step 7: Return document metadata
    return {
        "document_id": document_id,
        "filename": file.filename,
        "saved_as": saved_path.name,
        "pages": parsed_pdf["pages"],
        "characters": len(parsed_pdf["text"]),
        "chunks": len(chunks),
        "embeddings": len(embeddings),
        "stored": stored,
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "chunk_preview": [
            {
                "id": chunk.id,
                "length": chunk.length,
            }
            for chunk in chunks[:3]
        ],
        "status": "processed",
    }