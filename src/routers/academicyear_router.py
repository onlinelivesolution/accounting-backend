from typing import List

from fastapi import APIRouter, Depends, status

from src.schemas.academicyear_schema import (
    AcademicYearCreateDTO,
    AcademicYearDTO,
    AcademicYearUpdateDTO,
)

from src.services.interfaces.iacademicyear_service import (
    IAcademicYearService,
)

from src.depends.service_depends import (
    get_academicyear_service,
)

router = APIRouter(
    prefix="/academicYears",
    tags=["Academic Year"],
)


@router.get(
    "",
    response_model=List[AcademicYearDTO],
)
async def get_all_academic_years(
    service: IAcademicYearService = Depends(get_academicyear_service),
):
    return await service.get_all()


@router.get(
    "/current",
    response_model=AcademicYearDTO,
)
async def get_current_academic_year(
    service: IAcademicYearService = Depends(get_academicyear_service),
):
    return await service.get_current()


@router.get(
    "/{academic_year_id}",
    response_model=AcademicYearDTO,
)
async def get_academic_year(
    academic_year_id: int,
    service: IAcademicYearService = Depends(get_academicyear_service),
):
    return await service.get_by_id(academic_year_id)


@router.post(
    "",
    response_model=AcademicYearDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_academic_year(
    data: AcademicYearCreateDTO,
    service: IAcademicYearService = Depends(get_academicyear_service),
):
    return await service.create(data)


@router.put(
    "/{academic_year_id}",
    response_model=AcademicYearDTO,
)
async def update_academic_year(
    academic_year_id: int,
    data: AcademicYearUpdateDTO,
    service: IAcademicYearService = Depends(get_academicyear_service),
):
    return await service.update(
        academic_year_id,
        data,
    )


@router.put(
    "/{academic_year_id}/setCurrent",
    response_model=AcademicYearDTO,
)
async def set_current_academic_year(
    academic_year_id: int,
    service: IAcademicYearService = Depends(get_academicyear_service),
):
    return await service.set_current(academic_year_id)


@router.delete(
    "/{academic_year_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_academic_year(
    academic_year_id: int,
    service: IAcademicYearService = Depends(get_academicyear_service),
):
    await service.delete(academic_year_id)

    return None
