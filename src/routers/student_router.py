from typing import List
from fastapi import HTTPException
from fastapi import APIRouter, Depends, File, UploadFile, status
from src.core.auth_dependency import get_current_user
from src.schemas.student_schema import (
    StudentCreateDTO,
    StudentDTO,
    StudentUpdateDTO,
    StudentDropdownDTO,
)

from src.services.interfaces.istudent_service import (
    IStudentService,
)

from src.depends.service_depends import (
    get_student_service,
)

router = APIRouter(
    prefix="/api/students",
    tags=["Students"],
)


@router.get(
    "/getStudents",
    response_model=List[StudentDTO],
)
async def get_students(
    service: IStudentService = Depends(get_student_service),
):
    return await service.get_all()


@router.get("/next-student-code")
async def get_next_student_code(
    service: IStudentService = Depends(get_student_service),
):
    student_code = await service.get_next_student_code()

    return {"studentCode": student_code}


@router.get(
    "/dropdown",
    response_model=List[StudentDropdownDTO],
)
async def get_student_dropdown(
    service: IStudentService = Depends(get_student_service),
):
    return await service.get_dropdown_students()


@router.post("/{studentID}/photo")
async def upload_student_photo(
    studentID: int,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    service: IStudentService = Depends(get_student_service),
):
    print("========== CURRENT USER ==========")
    print(current_user)
    print("==================================")

    database_name = current_user.get("tenant")

    print("DATABASE NAME:", database_name)

    if not database_name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant database information is missing.",
        )

    return await service.upload_photo(
        studentID=studentID,
        file=file,
        database_name=database_name,
    )


# @router.post("/{studentID}/photo")
# async def upload_student_photo(
#     studentID: int,
#     file: UploadFile = File(...),
#     current_user=Depends(get_current_user),
#     service: IStudentService = Depends(get_student_service),
# ):
#     database_name = current_user.get("databaseName")

#     if not database_name:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Tenant database information is missing.",
#         )

#     return await service.upload_photo(
#         student_id=studentID,
#         file=file,
#         database_name=database_name,
#     )


@router.get(
    "/{student_id}",
    response_model=StudentDTO,
)
async def get_student(
    student_id: int,
    service: IStudentService = Depends(get_student_service),
):
    return await service.get_by_id(student_id)


@router.post(
    "",
    response_model=StudentDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    data: StudentCreateDTO,
    service: IStudentService = Depends(get_student_service),
):
    return await service.create(data)


@router.put(
    "/{student_id}",
    response_model=StudentDTO,
)
async def update_student(
    student_id: int,
    data: StudentUpdateDTO,
    service: IStudentService = Depends(get_student_service),
):
    return await service.update(
        student_id,
        data,
    )


@router.put(
    "/{student_id}/deactivate",
    response_model=StudentDTO,
)
async def deactivate_student(
    student_id: int,
    service: IStudentService = Depends(get_student_service),
):
    return await service.deactivate(student_id)
