from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from src.schemas.studentenrollment_schema import (
    StudentEnrollmentCreateDTO,
    StudentEnrollmentDTO,
    StudentEnrollmentUpdateDTO,
)
from src.models.studentenrollment import StudentEnrollment
from src.repositories.interfaces.istudentenrollment_repository import (
    IStudentEnrollmentRepository,
)
from src.services.interfaces.istudentenrollment_service import (
    IStudentEnrollmentService,
)


class StudentEnrollmentService(IStudentEnrollmentService):

    def __init__(
        self,
        repository: IStudentEnrollmentRepository,
    ):
        self.repository = repository

    async def create(
        self,
        data: StudentEnrollmentCreateDTO,
    ) -> StudentEnrollmentDTO:

        # Prevent duplicate enrollment for the same
        # student and academic year.
        existing = await self.repository.get_by_student_and_year(
            data.studentID,
            data.academicYearID,
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=("Student is already enrolled " "for this academic year."),
            )

        enrollment = StudentEnrollment(
            studentID=data.studentID,
            academicYearID=data.academicYearID,
            classID=data.classID,
            sectionID=data.sectionID,
            rollNo=data.rollNo,
            enrollmentDate=data.enrollmentDate,
            status=data.status,
            remarks=data.remarks,
            createdDate=datetime.now(),
        )

        created = await self.repository.create(enrollment)

        return StudentEnrollmentDTO.model_validate(created)

    async def get_by_id(
        self,
        enrollment_id: int,
    ) -> StudentEnrollmentDTO:

        enrollment = await self.repository.get_by_id(enrollment_id)

        if enrollment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student enrollment not found.",
            )

        return StudentEnrollmentDTO.model_validate(enrollment)

    async def get_all(
        self,
    ) -> List[StudentEnrollmentDTO]:

        enrollments = await self.repository.get_all()

        return [StudentEnrollmentDTO.model_validate(item) for item in enrollments]

    async def get_by_student(
        self,
        student_id: int,
    ) -> List[StudentEnrollmentDTO]:

        enrollments = await self.repository.get_by_student(student_id)

        return [StudentEnrollmentDTO.model_validate(item) for item in enrollments]

    async def update(
        self,
        enrollment_id: int,
        data: StudentEnrollmentUpdateDTO,
    ) -> StudentEnrollmentDTO:

        enrollment = await self.repository.get_by_id(enrollment_id)

        if enrollment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student enrollment not found.",
            )

        if (
            data.academicYearID is not None
            and data.academicYearID != enrollment.academicYearID
        ):

            existing = await self.repository.get_by_student_and_year(
                enrollment.studentID,
                data.academicYearID,
            )

            if existing is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=("Student is already enrolled " "for this academic year."),
                )

        if data.academicYearID is not None:
            enrollment.academicYearID = data.academicYearID

        if data.classID is not None:
            enrollment.classID = data.classID

        if data.sectionID is not None:
            enrollment.sectionID = data.sectionID

        if data.rollNo is not None:
            enrollment.rollNo = data.rollNo

        if data.enrollmentDate is not None:
            enrollment.enrollmentDate = data.enrollmentDate

        if data.status is not None:
            enrollment.status = data.status

        if data.remarks is not None:
            enrollment.remarks = data.remarks

        enrollment.updatedDate = datetime.now()

        updated = await self.repository.update(enrollment)

        return StudentEnrollmentDTO.model_validate(updated)

    async def deactivate(
        self,
        enrollment_id: int,
    ) -> StudentEnrollmentDTO:

        enrollment = await self.repository.get_by_id(enrollment_id)

        if enrollment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student enrollment not found.",
            )

        updated = await self.repository.deactivate(enrollment)

        return StudentEnrollmentDTO.model_validate(updated)
