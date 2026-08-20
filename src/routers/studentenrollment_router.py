from typing import List

from fastapi import APIRouter, Depends

from src.schemas.studentenrollment_schema import (
    StudentEnrollmentCreateDTO,
    StudentEnrollmentDTO,
    StudentEnrollmentUpdateDTO,
)
from src.depends.service_depends import (
    get_student_enrollment_service,
)

from src.services.interfaces.istudentenrollment_service import (
    IStudentEnrollmentService,
)

router = APIRouter(
    prefix="/api/student-enrollments",
    tags=["Student Enrollment"],
)


@router.post(
    "",
    response_model=StudentEnrollmentDTO,
)
async def create_student_enrollment(
    data: StudentEnrollmentCreateDTO,
    service: IStudentEnrollmentService = Depends(get_student_enrollment_service),
):
    return await service.create(data)


@router.get(
    "",
    response_model=List[StudentEnrollmentDTO],
)
async def get_all_student_enrollments(
    service: IStudentEnrollmentService = Depends(get_student_enrollment_service),
):
    return await service.get_all()


@router.get(
    "/student/{student_id}",
    response_model=List[StudentEnrollmentDTO],
)
async def get_student_enrollments(
    student_id: int,
    service: IStudentEnrollmentService = Depends(get_student_enrollment_service),
):
    return await service.get_by_student(student_id)


@router.get(
    "/{enrollment_id}",
    response_model=StudentEnrollmentDTO,
)
async def get_student_enrollment(
    enrollment_id: int,
    service: IStudentEnrollmentService = Depends(get_student_enrollment_service),
):
    return await service.get_by_id(enrollment_id)


@router.put(
    "/{enrollment_id}",
    response_model=StudentEnrollmentDTO,
)
async def update_student_enrollment(
    enrollment_id: int,
    data: StudentEnrollmentUpdateDTO,
    service: IStudentEnrollmentService = Depends(get_student_enrollment_service),
):
    return await service.update(
        enrollment_id,
        data,
    )


@router.patch(
    "/{enrollment_id}/deactivate",
    response_model=StudentEnrollmentDTO,
)
async def deactivate_student_enrollment(
    enrollment_id: int,
    service: IStudentEnrollmentService = Depends(get_student_enrollment_service),
):
    return await service.deactivate(enrollment_id)
