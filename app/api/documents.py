from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.file_storage import FileStorageService
from app.services.pdf_parser import PDFParserService
from app.services.chunking import ChunkingService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

storage = FileStorageService()
parser = PDFParserService()
chunker = ChunkingService()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    # Step 1: Save uploaded file
    saved_path = await storage.save_file(file)

    # Step 2: Extract text from PDF
    parsed_pdf = parser.extract_text(saved_path)

    # Step 3: Create chunks
    chunks = chunker.create_chunks(parsed_pdf["text"])

    # Step 4: Return document metadata
    return {
        "filename": file.filename,
        "saved_as": saved_path.name,
        "pages": parsed_pdf["pages"],
        "characters": len(parsed_pdf["text"]),
        "chunks": len(chunks),
        "chunk_preview": [
            {
                "id": chunk.id,
                "length": chunk.length,
            }
            for chunk in chunks[:3]
        ],
        "status": "processed",
    }