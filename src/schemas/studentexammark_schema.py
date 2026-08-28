from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StudentExamMarkCreateDTO(BaseModel):
    examID: int
    examSubjectID: int
    studentID: int

    writtenMarks: Decimal = Field(
        default=0,
        ge=0
    )

    mcqMarks: Decimal = Field(
        default=0,
        ge=0
    )

    practicalMarks: Decimal = Field(
        default=0,
        ge=0
    )

    vivaMarks: Decimal = Field(
        default=0,
        ge=0
    )

    remarks: Optional[str] = None

    status: str = "Draft"


class StudentExamMarkUpdateDTO(BaseModel):
    writtenMarks: Optional[Decimal] = Field(
        default=None,
        ge=0
    )

    mcqMarks: Optional[Decimal] = Field(
        default=None,
        ge=0
    )

    practicalMarks: Optional[Decimal] = Field(
        default=None,
        ge=0
    )

    vivaMarks: Optional[Decimal] = Field(
        default=None,
        ge=0
    )

    remarks: Optional[str] = None
    status: Optional[str] = None


class StudentExamMarkDTO(BaseModel):
    markID: int

    examID: int
    examSubjectID: int
    studentID: int

    writtenMarks: Decimal
    mcqMarks: Decimal
    practicalMarks: Decimal
    vivaMarks: Decimal

    totalMarks: Decimal

    isPassed: Optional[bool] = None

    remarks: Optional[str] = None

    isLocked: bool

    status: str

    createdDate: datetime
    updatedDate: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)