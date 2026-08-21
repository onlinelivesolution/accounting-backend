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
    StudentDropdownDTO,
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

        return [StudentDTO.model_validate(student) for student in students]

    async def get_by_id(
        self,
        student_id: int,
    ) -> StudentDTO:

        student = await self.repository.get_by_id(student_id)

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

        # ---------------------------------------------------------
        # Check duplicate admission number
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # Temporary student code
        #
        # studentCode is NOT NULL in SQL Server, so we need to
        # provide a temporary unique value until SQL Server
        # generates studentID.
        # ---------------------------------------------------------
        temporary_code = (
            f"TEMP-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        )

        student = Student(
            studentCode=temporary_code,
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

        # ---------------------------------------------------------
        # Insert and FLUSH
        #
        # SQL Server now generates studentID.
        # ---------------------------------------------------------
        created = await self.repository.create(student)

        # ---------------------------------------------------------
        # Generate the REAL student code
        #
        # Example:
        # studentID = 51
        # year = 2026
        #
        # STU-2026-000051
        # ---------------------------------------------------------
        current_year = datetime.now().year

        created.studentCode = (
            f"STU-{current_year}-{created.studentID:06d}"
        )

        # ---------------------------------------------------------
        # Commit
        # ---------------------------------------------------------
        await self.repository.db.commit()

        await self.repository.db.refresh(created)

        return StudentDTO.model_validate(created)
    
    async def update(
        self,
        student_id: int,
        data: StudentUpdateDTO,
    ) -> StudentDTO:

        student = await self.repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found.",
            )

        if data.studentCode is not None:

            existing = await self.repository.get_by_student_code(data.studentCode)

            if existing is not None and existing.studentID != student_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(f"Student code " f"{data.studentCode} already exists."),
                )

            student.studentCode = data.studentCode

        if data.admissionNo is not None:

            existing = await self.repository.get_by_admission_no(data.admissionNo)

            if existing is not None and existing.studentID != student_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(f"Admission number " f"{data.admissionNo} already exists."),
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

        student = await self.repository.get_by_id(student_id)

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
    
    async def get_next_student_code(self) -> str:

        # Get the next student ID
        next_student_id = (
            await self.repository.get_next_student_id()
        )

        # Current year
        current_year = datetime.now().year

        # Generate preview code
        student_code = (
            f"STU-{current_year}-{next_student_id:06d}"
        )

        return student_code
    
    async def get_dropdown_students(
        self,
    ) -> list[StudentDropdownDTO]:

        students = await self.repository.get_dropdown_students()

        result = []

        for student in students:

            full_name = " ".join(
                filter(
                    None,
                    [
                        student.firstName,
                        student.middleName,
                        student.lastName,
                    ],
                )
            )

            result.append(
                StudentDropdownDTO(
                    studentID=student.studentID,
                    studentCode=student.studentCode,
                    studentName=full_name,
                    admissionNo=student.admissionNo,
                )
            )

        return result
