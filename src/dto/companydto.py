from pydantic import BaseModel, ConfigDict

class CompanyDTO(BaseModel):
    companyCode: str
    companyName: str

    model_config = ConfigDict(from_attributes=True)