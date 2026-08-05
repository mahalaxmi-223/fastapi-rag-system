import fitz
from pathlib import Path


class PDFParserService:
    """
    Service responsible for extracting text from PDF files.
    """

    def extract_text(self, pdf_path: Path) -> dict:
        """
        Extract text from every page of a PDF.

        Returns:
            {
                "pages": int,
                "text": str
            }
        """

        document = fitz.open(pdf_path)

        text = []

        for page in document:
            text.append(page.get_text())

        document.close()

        return {
            "pages": len(text),
            "text": "\n".join(text)
        }