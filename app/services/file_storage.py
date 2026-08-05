from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = Path("data/uploads")


class FileStorageService:
    """
    Service responsible for saving uploaded files.
    """

    def __init__(self):
        # Create the uploads directory if it doesn't exist
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile) -> Path:
        """
        Save the uploaded file to disk.

        Returns:
            Path: Location where the file was saved.
        """

        # Extract original extension
        extension = Path(file.filename).suffix

        # Generate unique filename
        unique_filename = f"{uuid4()}{extension}"

        file_path = UPLOAD_DIR / unique_filename

        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path