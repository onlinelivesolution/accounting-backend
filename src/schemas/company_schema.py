from pydantic import BaseModel, ConfigDict

class CompanyDropdown(BaseModel):
    companyCode: str
    companyName: str

    model_config = ConfigDict(from_attributes=True)