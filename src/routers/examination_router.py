## `src/router/examination_router.py`

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from src.services.interfaces.iexamination_service import IExaminationService
from src.depends.service_depends import get_examination_service

from src.schemas.examination_schema import (
    ExaminationCreateDTO,
    ExaminationDTO,
    ExaminationUpdateDTO,
)

from src.repositories.examination_repository import (
    ExaminationRepository,
)

from src.services.examination_service import (
    ExaminationService,
)


router = APIRouter(
    prefix="/api/examinations",
    tags=["Examinations"],
)


# ============================================================
# CREATE EXAMINATION
# ============================================================

@router.post("/createExamination",
    response_model=ExaminationDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_examination(
    data: ExaminationCreateDTO,
    service: IExaminationService = Depends(
        get_examination_service
    ),
):
    try:

        return await service.create(data)

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ============================================================
# GET ALL EXAMINATIONS
# ============================================================

@router.get(
    "",
    response_model=List[ExaminationDTO],
)
async def get_all_examinations(
    service: ExaminationService = Depends(
        get_examination_service
    ),
):
    try:

        return await service.get_all()

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ============================================================
# GET EXAMINATION BY ID
# ============================================================

@router.get(
    "/{examID}",
    response_model=ExaminationDTO,
)
async def get_examination(
    examID: int,
    service: ExaminationService = Depends(
        get_examination_service
    ),
):
    try:

        examination = await service.get_by_id(
            examID
        )

        if examination is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Examination with ID "
                    f"{examID} not found."
                ),
            )

        return examination

    except HTTPException:
        raise

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ============================================================
# GET EXAMINATIONS BY ACADEMIC YEAR
# ============================================================

@router.get(
    "/academic-year/{academicYearID}",
    response_model=List[ExaminationDTO],
)
async def get_examinations_by_academic_year(
    academicYearID: int,
    service: ExaminationService = Depends(
        get_examination_service
    ),
):
    try:

        return await service.get_by_academic_year(
            academicYearID
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ============================================================
# UPDATE EXAMINATION
# ============================================================

@router.put(
    "/{examID}",
    response_model=ExaminationDTO,
)
async def update_examination(
    examID: int,
    data: ExaminationUpdateDTO,
    service: ExaminationService = Depends(
        get_examination_service
    ),
):
    try:

        return await service.update(
            examID,
            data
        )

    except ValueError as exc:

        message = str(exc)

        if "not found" in message.lower():

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


# ============================================================
# DEACTIVATE EXAMINATION
# ============================================================

@router.delete(
    "/{examID}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deactivate_examination(
    examID: int,
    service: ExaminationService = Depends(
        get_examination_service
    ),
):
    try:

        result = await service.deactivate(
            examID
        )

        if not result:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Examination with ID "
                    f"{examID} not found."
                ),
            )

        return None

    except HTTPException:
        raise

    except ValueError as exc:

        message = str(exc)

        if "not found" in message.lower():

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )