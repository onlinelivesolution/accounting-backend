from datetime import datetime
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from fastapi import HTTPException, status

from src.schemas.academicyear_schema import (
    AcademicYearCreateDTO,
    AcademicYearDTO,
    AcademicYearUpdateDTO,
)

from src.models.academicyear import AcademicYear

from src.repositories.interfaces.iacademicyear_repository import (
    IAcademicYearRepository,
)

from src.services.interfaces.iacademicyear_service import (
    IAcademicYearService,
)


class AcademicYearService(IAcademicYearService):

    def __init__(
        self,
        repository: IAcademicYearRepository,
    ):
        self.repository = repository

    async def get_all(self) -> List[AcademicYearDTO]:

        academic_years = await self.repository.get_all()

        return [
            AcademicYearDTO.model_validate(academic_year)
            for academic_year in academic_years
        ]

    async def get_by_id(self, academic_year_id: int) -> AcademicYearDTO:

        academic_year = await self.repository.get_by_id(academic_year_id)

        if academic_year is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Academic year not found."
            )

        return AcademicYearDTO.model_validate(academic_year)

    async def get_by_year(
        self,
        year: int,
    ):
        return await self.repository.get_by_year(year)

    async def get_current(self) -> AcademicYearDTO:

        academic_year = await self.repository.get_current()

        if academic_year is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No current academic year has been configured.",
            )

        return AcademicYearDTO.model_validate(academic_year)

    async def create(
        self,
        data: AcademicYearCreateDTO,
    ) -> AcademicYearDTO:

        if data.startDate >= data.endDate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date.",
            )

        existing = await self.repository.get_by_year(
            data.year
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Academic year {data.year} already exists.",
            )

        current = await self.repository.get_current()

        is_current = data.isCurrent

        if current is None:
            is_current = True

        if is_current and current is not None:
            current.isCurrent = False
            current.updatedDate = datetime.now()

        academic_year = AcademicYear(
            year=data.year,
            name=data.name,
            startDate=data.startDate,
            endDate=data.endDate,
            isCurrent=is_current,
            status=data.status,
            createdDate=datetime.now(),
        )

        created = await self.repository.create(
            academic_year
        )

        return AcademicYearDTO.model_validate(created)

    async def update(
        self, academic_year_id: int, data: AcademicYearUpdateDTO
    ) -> AcademicYearDTO:

        academic_year = await self.repository.get_by_id(academic_year_id)

        if academic_year is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Academic year not found."
            )

        # Validate dates if provided
        start_date = (
            data.startDate if data.startDate is not None else academic_year.startDate
        )

        end_date = data.endDate if data.endDate is not None else academic_year.endDate

        if start_date >= end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date.",
            )

        # Update fields
        if data.name is not None:
            academic_year.name = data.name

        if data.startDate is not None:
            academic_year.startDate = data.startDate

        if data.endDate is not None:
            academic_year.endDate = data.endDate

        if data.status is not None:
            academic_year.status = data.status

        # Handle current year
        if data.isCurrent is True:

            current = await self.repository.get_current()

            if current is not None and current.academicYearID != academic_year_id:
                current.isCurrent = False
                current.updatedDate = datetime.now()

            academic_year.isCurrent = True

        elif data.isCurrent is False:

            # Don't allow removing the current flag
            # without selecting another current year.
            if academic_year.isCurrent:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "The current academic year cannot be "
                        "deactivated as current. Set another "
                        "academic year as current first."
                    ),
                )

            academic_year.isCurrent = False

        academic_year.updatedDate = datetime.now()

        updated = await self.repository.update(academic_year)

        return AcademicYearDTO.model_validate(updated)

    async def set_current(self, academic_year_id: int) -> AcademicYearDTO:

        academic_year = await self.repository.get_by_id(academic_year_id)

        if academic_year is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Academic year not found."
            )

        if academic_year.status != "Active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=("An inactive academic year cannot " "be set as current."),
            )

        current = await self.repository.get_current()

        if current is not None and current.academicYearID != academic_year_id:
            current.isCurrent = False
            current.updatedDate = datetime.now()

        academic_year.isCurrent = True
        academic_year.updatedDate = datetime.now()

        updated = await self.repository.update(academic_year)

        return AcademicYearDTO.model_validate(updated)



    async def deactivate(
        self,
        academic_year_id: int,
    ) -> AcademicYearDTO:

        academic_year = await self.repository.get_by_id(
            academic_year_id
        )

        if academic_year is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Academic year not found.",
            )

        if academic_year.isCurrent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "The current academic year cannot be "
                    "deactivated."
                ),
            )

        if academic_year.status == "Inactive":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Academic year is already inactive.",
            )

        # SOFT DELETE
        academic_year.status = "Inactive"
        academic_year.updatedDate = datetime.now()

        updated = await self.repository.update(
            academic_year
        )

        return AcademicYearDTO.model_validate(updated)
