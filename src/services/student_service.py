from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from src.models.student import Student

from src.repositories.interfaces.istudent_repository import (
    IStudentRepository,
)

from src.schemas.student_schema import (
    StudentCreateDTO,
    StudentDTO,
    StudentUpdateDTO,
)

from src.services.interfaces.istudent_service import (
    IStudentService,
)


class StudentService(IStudentService):

    def __init__(
        self,
        repository: IStudentRepository,
    ):
        self.repository = repository

    async def get_all(self) -> List[StudentDTO]:

        students = await self.repository.get_all()

        return [
            StudentDTO.model_validate(student)
            for student in students
        ]

    async def get_by_id(
        self,
        student_id: int,
    ) -> StudentDTO:

        student = await self.repository.get_by_id(
            student_id
        )

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found.",
            )

        return StudentDTO.model_validate(student)

    async def create(
        self,
        data: StudentCreateDTO,
    ) -> StudentDTO:

        # Check duplicate student code
        existing = await self.repository.get_by_student_code(
            data.studentCode
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Student code "
                    f"{data.studentCode} already exists."
                ),
            )

        # Check duplicate admission number
        existing = await self.repository.get_by_admission_no(
            data.admissionNo
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Admission number "
                    f"{data.admissionNo} already exists."
                ),
            )

        student = Student(
            studentCode=data.studentCode,
            admissionNo=data.admissionNo,
            firstName=data.firstName,
            middleName=data.middleName,
            lastName=data.lastName,
            dateOfBirth=data.dateOfBirth,
            gender=data.gender,
            bloodGroup=data.bloodGroup,
            photoPath=data.photoPath,
            phone=data.phone,
            email=data.email,
            address=data.address,
            city=data.city,
            postalCode=data.postalCode,
            admissionDate=data.admissionDate,
            status="Active",
            createdDate=datetime.now(),
        )

        created = await self.repository.create(student)

        return StudentDTO.model_validate(created)

    async def update(
        self,
        student_id: int,
        data: StudentUpdateDTO,
    ) -> StudentDTO:

        student = await self.repository.get_by_id(
            student_id
        )

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found.",
            )

        if data.studentCode is not None:

            existing = (
                await self.repository.get_by_student_code(
                    data.studentCode
                )
            )

            if (
                existing is not None
                and existing.studentID != student_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Student code "
                        f"{data.studentCode} already exists."
                    ),
                )

            student.studentCode = data.studentCode

        if data.admissionNo is not None:

            existing = (
                await self.repository.get_by_admission_no(
                    data.admissionNo
                )
            )

            if (
                existing is not None
                and existing.studentID != student_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Admission number "
                        f"{data.admissionNo} already exists."
                    ),
                )

            student.admissionNo = data.admissionNo

        if data.firstName is not None:
            student.firstName = data.firstName

        if data.middleName is not None:
            student.middleName = data.middleName

        if data.lastName is not None:
            student.lastName = data.lastName

        if data.dateOfBirth is not None:
            student.dateOfBirth = data.dateOfBirth

        if data.gender is not None:
            student.gender = data.gender

        if data.bloodGroup is not None:
            student.bloodGroup = data.bloodGroup

        if data.photoPath is not None:
            student.photoPath = data.photoPath

        if data.phone is not None:
            student.phone = data.phone

        if data.email is not None:
            student.email = data.email

        if data.address is not None:
            student.address = data.address

        if data.city is not None:
            student.city = data.city

        if data.postalCode is not None:
            student.postalCode = data.postalCode

        if data.admissionDate is not None:
            student.admissionDate = data.admissionDate

        if data.status is not None:
            student.status = data.status

        student.updatedDate = datetime.now()

        updated = await self.repository.update(student)

        return StudentDTO.model_validate(updated)

    async def deactivate(
        self,
        student_id: int,
    ) -> StudentDTO:

        student = await self.repository.get_by_id(
            student_id
        )

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found.",
            )

        if student.status == "Inactive":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is already inactive.",
            )

        student.status = "Inactive"
        student.updatedDate = datetime.now()

        updated = await self.repository.update(student)

        return StudentDTO.model_validate(updated)