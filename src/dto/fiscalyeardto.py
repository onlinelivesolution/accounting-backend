from pydantic import BaseModel, ConfigDict

class FiscalYearDTO(BaseModel):
    finYearID: int
    finYear: str

    model_config = ConfigDict(from_attributes=True)