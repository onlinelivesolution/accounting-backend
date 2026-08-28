from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExamScheduleCreateDTO(BaseModel):
    examID: int
    examSubjectID: int

    examDate: date
    startTime: time
    endTime: time

    roomNo: Optional[str] = None
    instructions: Optional[str] = None

    status: str = "Active"


class ExamScheduleUpdateDTO(BaseModel):
    examSubjectID: Optional[int] = None

    examDate: Optional[date] = None
    startTime: Optional[time] = None
    endTime: Optional[time] = None

    roomNo: Optional[str] = None
    instructions: Optional[str] = None

    status: Optional[str] = None


class ExamScheduleDTO(BaseModel):
    examScheduleID: int
    examID: int
    examSubjectID: int

    examDate: date
    startTime: time
    endTime: time

    roomNo: Optional[str] = None
    instructions: Optional[str] = None

    status: str
    createdDate: datetime
    updatedDate: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)