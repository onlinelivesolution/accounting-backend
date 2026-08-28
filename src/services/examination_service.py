from datetime import datetime
from typing import List, Optional

from src.schemas.examination_schema import (
    ExaminationCreateDTO,
    ExaminationDTO,
    ExaminationUpdateDTO,
)
from src.models.examination import Examination
from src.repositories.interfaces.iexamination_repository import (
    IExaminationRepository,
)
from src.services.interfaces.iexamination_service import (
    IExaminationService,
)


class ExaminationService(IExaminationService):

    def __init__(
        self,
        repository: IExaminationRepository
    ):
        self.repository = repository

    # =========================================================
    # CREATE
    # =========================================================

    async def create(
        self,
        data: ExaminationCreateDTO
    ) -> ExaminationDTO:

        examination = Examination(
            academicYearID=data.academicYearID,
            examName=data.examName,
            examType=data.examType,
            startDate=data.startDate,
            endDate=data.endDate,
            status=data.status or "Active",
            createdDate=datetime.utcnow(),
        )

        created = await self.repository.create(
            examination
        )

        return ExaminationDTO.model_validate(
            created
        )

    # =========================================================
    # GET BY ID
    # =========================================================

    async def get_by_id(
        self,
        examID: int
    ) -> Optional[ExaminationDTO]:

        examination = await self.repository.get_by_id(
            examID
        )

        if examination is None:
            return None

        return ExaminationDTO.model_validate(
            examination
        )

    # =========================================================
    # GET ALL
    # =========================================================

    async def get_all(
        self
    ) -> List[ExaminationDTO]:

        examinations = await self.repository.get_all()

        return [
            ExaminationDTO.model_validate(
                examination
            )
            for examination in examinations
        ]

    # =========================================================
    # GET BY ACADEMIC YEAR
    # =========================================================

    async def get_by_academic_year(
        self,
        academicYearID: int
    ) -> List[ExaminationDTO]:

        examinations = (
            await self.repository.get_by_academic_year(
                academicYearID
            )
        )

        return [
            ExaminationDTO.model_validate(
                examination
            )
            for examination in examinations
        ]

    # =========================================================
    # UPDATE
    # =========================================================

    async def update(
        self,
        examID: int,
        data: ExaminationUpdateDTO
    ) -> ExaminationDTO:

        # -----------------------------------------------------
        # Find existing examination
        # -----------------------------------------------------

        examination = await self.repository.get_by_id(
            examID
        )

        if examination is None:
            raise ValueError(
                f"Examination with ID {examID} not found."
            )

        # -----------------------------------------------------
        # Calculate final values for validation
        # -----------------------------------------------------

        finalStartDate = (
            data.startDate
            if data.startDate is not None
            else examination.startDate
        )

        finalEndDate = (
            data.endDate
            if data.endDate is not None
            else examination.endDate
        )

        if (
            finalStartDate is not None
            and finalEndDate is not None
            and finalStartDate > finalEndDate
        ):
            raise ValueError(
                "Start date cannot be greater than end date."
            )

        # -----------------------------------------------------
        # Update academic year
        # -----------------------------------------------------

        if data.academicYearID is not None:
            examination.academicYearID = (
                data.academicYearID
            )

        # -----------------------------------------------------
        # Update exam name
        # -----------------------------------------------------

        if data.examName is not None:

            examName = data.examName.strip()

            if not examName:
                raise ValueError(
                    "Exam name cannot be empty."
                )

            examination.examName = examName

        # -----------------------------------------------------
        # Update exam type
        # -----------------------------------------------------

        if data.examType is not None:

            examType = data.examType.strip()

            if not examType:
                raise ValueError(
                    "Exam type cannot be empty."
                )

            examination.examType = examType

        # -----------------------------------------------------
        # Update dates
        # -----------------------------------------------------

        if data.startDate is not None:
            examination.startDate = data.startDate

        if data.endDate is not None:
            examination.endDate = data.endDate

        # -----------------------------------------------------
        # Update status
        # -----------------------------------------------------

        if data.status is not None:
            examination.status = data.status

        # -----------------------------------------------------
        # Updated date
        # -----------------------------------------------------

        examination.updatedDate = datetime.utcnow()

        # -----------------------------------------------------
        # Save
        # -----------------------------------------------------

        updated = await self.repository.update(
            examination
        )

        return ExaminationDTO.model_validate(
            updated
        )

    # =========================================================
    # DEACTIVATE
    # =========================================================

    async def deactivate(
        self,
        examID: int
    ) -> bool:

        examination = await self.repository.get_by_id(
            examID
        )

        if examination is None:
            raise ValueError(
                f"Examination with ID {examID} not found."
            )

        # -----------------------------------------------------
        # Already inactive
        # -----------------------------------------------------

        if examination.status == "Inactive":
            raise ValueError(
                "Examination is already inactive."
            )

        # -----------------------------------------------------
        # Deactivate
        # -----------------------------------------------------

        return await self.repository.deactivate(
            examID
        )