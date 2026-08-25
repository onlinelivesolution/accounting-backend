from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import (
    HTTPException,
    UploadFile,
    status,
)


class TenantBannerService:

    ALLOWED_TYPES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024

    BASE_UPLOAD_DIR = Path("uploads") / "tenants"

    async def save_banner(
        self,
        file: UploadFile,
        tenant_name: str,
    ) -> str:

        # -----------------------------------------
        # Validate tenant
        # -----------------------------------------

        if not tenant_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant information is required.",
            )

        # -----------------------------------------
        # Validate file type
        # -----------------------------------------

        if file.content_type not in self.ALLOWED_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid banner format. " "Only JPG, PNG and WEBP are allowed."
                ),
            )

        # -----------------------------------------
        # Read file
        # -----------------------------------------

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant banner is empty.",
            )

        # -----------------------------------------
        # Validate size
        # -----------------------------------------

        if len(content) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant banner must not exceed 5 MB.",
            )

        # -----------------------------------------
        # Current year
        # -----------------------------------------

        year = datetime.now().year

        # -----------------------------------------
        # File extension
        # -----------------------------------------

        extension = self.ALLOWED_TYPES[file.content_type]

        # -----------------------------------------
        # Generate filename
        # -----------------------------------------

        filename = f"banner_" f"{uuid4().hex}" f"{extension}"

        # -----------------------------------------
        # Tenant directory
        #
        # uploads/
        #   tenants/
        #     sales2_gmail_com/
        #       banner/
        #         2026/
        # -----------------------------------------

        directory = self.BASE_UPLOAD_DIR / tenant_name / "banner" / str(year)

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -----------------------------------------
        # Save physical file
        # -----------------------------------------

        file_path = directory / filename

        file_path.write_bytes(content)

        # -----------------------------------------
        # Database relative path
        # -----------------------------------------

        return f"tenants/" f"{tenant_name}/" f"banner/" f"{year}/" f"{filename}"
