from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ExamSubjectCreateDTO(BaseModel):
    examID: int
    classSubjectID: int

    fullMarks: Decimal = Field(
        ...,
        gt=0
    )

    passMarks: Decimal = Field(
        ...,
        ge=0
    )

    isOptional: bool = False
    status: str = "Active"


class ExamSubjectUpdateDTO(BaseModel):
    classSubjectID: Optional[int] = None

    fullMarks: Optional[Decimal] = Field(
        default=None,
        gt=0
    )

    passMarks: Optional[Decimal] = Field(
        default=None,
        ge=0
    )

    isOptional: Optional[bool] = None
    status: Optional[str] = None


class ExamSubjectDTO(BaseModel):
    examSubjectID: int
    examID: int
    classSubjectID: int
    fullMarks: Decimal
    passMarks: Decimal
    isOptional: bool
    status: str
    createdDate: datetime

    model_config = ConfigDict(from_attributes=True)