from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StudentDocumentCreateDTO(BaseModel):

    studentID: int

    documentType: str = Field(..., max_length=50)

    documentName: str = Field(..., max_length=200)

    fileName: str | None = Field(default=None, max_length=255)

    filePath: str | None = Field(default=None, max_length=500)

    fileExtension: str | None = Field(default=None, max_length=20)

    description: str | None = Field(default=None, max_length=500)

    status: str = Field(default="Active", max_length=20)


class StudentDocumentUpdateDTO(BaseModel):

    documentType: str | None = Field(default=None, max_length=50)

    documentName: str | None = Field(default=None, max_length=200)

    fileName: str | None = Field(default=None, max_length=255)

    filePath: str | None = Field(default=None, max_length=500)

    fileExtension: str | None = Field(default=None, max_length=20)

    description: str | None = Field(default=None, max_length=500)

    status: str | None = Field(default=None, max_length=20)


class StudentDocumentDTO(BaseModel):

    documentID: int

    studentID: int

    documentType: str

    documentName: str

    fileName: str | None = None

    filePath: str | None = None

    fileExtension: str | None = None

    description: str | None = None

    uploadedDate: datetime

    status: str

    model_config = ConfigDict(from_attributes=True)
