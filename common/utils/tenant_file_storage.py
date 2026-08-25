from pathlib import Path
from uuid import uuid4

BASE_UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads" / "tenants"


def get_student_photo_directory(
    database_name: str,
    year: int,
) -> Path:

    directory = BASE_UPLOAD_DIR / database_name / "students" / str(year)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def generate_student_photo_filename(
    student_id: int,
    extension: str,
) -> str:

    unique_id = uuid4().hex

    return f"{student_id}_{unique_id}" f"{extension}"
