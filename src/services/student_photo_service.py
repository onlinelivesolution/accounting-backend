from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import (
    HTTPException,
    UploadFile,
    status,
)


class StudentPhotoService:

    ALLOWED_TYPES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024

    async def save_photo(
        self,
        file: UploadFile,
        studentID: int,
    ) -> str:

        # ----------------------------------------
        # Validate file type
        # ----------------------------------------

        if file.content_type not in self.ALLOWED_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=("Invalid photo format. " "Only JPG, PNG and WEBP are allowed."),
            )

        # ----------------------------------------
        # Read file
        # ----------------------------------------

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student photo is empty.",
            )

        # ----------------------------------------
        # Validate size
        # ----------------------------------------

        if len(content) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student photo must not exceed 5 MB.",
            )

        # ----------------------------------------
        # Generate filename
        # ----------------------------------------

        extension = self.ALLOWED_TYPES[file.content_type]

        filename = f"{studentID}_" f"{uuid4().hex}" f"{extension}"

        # ----------------------------------------
        # Current year
        # ----------------------------------------

        year = datetime.now().year

        # ----------------------------------------
        # Physical directory
        # ----------------------------------------

        directory = Path("uploads") / "students" / str(year)

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ----------------------------------------
        # Save physical file
        # ----------------------------------------

        file_path = directory / filename

        file_path.write_bytes(content)

        # ----------------------------------------
        # Database relative path
        # ----------------------------------------

        return f"students/" f"{year}/" f"{filename}"
